"""This module handles creating a new appointment.

Steps:
1. Find participant data, or create new Participant object if no existing data
   is found
2. Check if the participant is eligible for the given experiment
3. If yes, create the appointment
4. If no, return human friendly explanations why the participant is not eligible
"""
from typing import List, Tuple
import urllib.parse as parse

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.validators import ValidationError, validate_email
from django.utils.dateparse import parse_date
from uil.core.utils.mail import send_template_email

from comments.utils import add_system_comment
from experiments.models import Appointment, DefaultCriteria, Experiment, \
    TimeSlot
from experiments.utils.exclusion import build_exclusion_filters, \
    check_default_criteria, should_exclude_by_age
from main.utils import get_supreme_admin
from participants.models import CriterionAnswer, Participant
from .common import x_or_else

DEFAULT_INVALID_MESSAGES = {
    'language':         'Je kunt niet meedoen met het experiment omdat je '
                        'moedertaal niet overeen komt met de criteria voor '
                        'dit experiment. Als je denkt dat dit niet klopt, '
                        'neem dan even contact op met {}.',

    'multilingual_yes': 'Je kunt niet meedoen met het experiment omdat je '
                        'niet meertalig bent. Om mee te doen aan dit '
                        'experiment moet je meertalig zijn. Als je denkt dat '
                        'dit niet klopt, neem dan even contact op met {}.',
    'multilingual_no':  'Je kunt niet meedoen met het experiment omdat je '
                        'meertalig bent. Om mee te doen aan dit experiment '
                        'mag je niet meertalig zijn. Als je denkt dat '
                        'dit niet klopt, neem dan even contact op met {}.',
    'sex':              'Je kunt niet meedoen met het experiment omdat je '
                        'geslacht niet overeen komt met de criteria voor '
                        'dit experiment. Als je denkt dat dit niet klopt, '
                        'neem dan even contact op met {}.',
    'handedness':       'Je kunt niet meedoen met het experiment omdat je '
                        'voorkeurshand niet overeen komt met de criteria voor '
                        'dit experiment. Als je denkt dat dit niet klopt, '
                        'neem dan even contact op met {}.',
    'age':              'Je kunt niet meedoen met het experiment omdat je '
                        'leeftijd niet overeen komt met de criteria voor '
                        'dit experiment. Als je denkt dat dit niet klopt, '
                        'neem dan even contact op met {}.',
    'dyslexic_yes':     'Je kunt niet meedoen met het experiment omdat je '
                        'volgens onze gegevens niet dyslectisch bent.  Als je '
                        'denkt dat dit niet klopt, neem dan even contact op '
                        'met {}.',
    'dyslexic_no':      'Je kunt niet meedoen met het experiment omdat je '
                        'volgens onze gegevens dyslectisch bent. Als je denkt '
                        'dat dit niet klopt, neem dan even contact op met {}.',
    'social_status_S':  'Je kunt niet meedoen met het experiment omdat je '
                        'volgens onze gegevens niet student bent. Als je '
                        'denkt dat dit niet klopt, neem dan even contact op '
                        'met {}.',
    'social_status_O':  'Je kunt niet meedoen met het experiment omdat je '
                        'volgens onze gegevens student bent. Als je denkt '
                        'dat dit niet klopt, neem dan even contact op met {}.',
}

MISC_INVALID_MESSAGES = {
    'email':              "Je hebt geen geldig email adres ingevuld! Probeer "
                          "opnieuw.",
    'timeslot':           "Aanmelding mislukt: sorry, dit tijdstip is al door "
                          "iemand anders gereserveerd! Probeer opnieuw.",
    'invalid_experiment': "Je hebt al meegedaan met een eerdere versie "
                          "van dit experiment en kunt helaas niet nog een "
                          "keer meedoen. Dankjewel voor je belangstelling!",
    'incapable':          "De beheerder heeft je uitgesloten van het deelnemen "
                          "aan experimenten. Hier kunnen verschillende redenen "
                          "voor zijn; de meest waarschijnlijke is dat je een "
                          "aantal keer niet bent komen opdagen voor een "
                          "afspraak. Als je toch nog mee wilt doen, neem dan "
                          "contact op met {}"
}


def register_participant(data: dict, experiment: Experiment) -> Tuple[bool,
                                                                      bool,
                                                                      list]:
    default_criteria = experiment.defaultcriteria

    try:
        time_slot = experiment.timeslot_set.get(pk=data.get('timeslot'))
    except TimeSlot.DoesNotExist:
        time_slot = None

    participant = _get_participant(data)

    # Incapable participants get direct rejection
    if not participant.capable:
        return False, False, [
            _format_message(MISC_INVALID_MESSAGES['incapable'])
        ]

    invalid_default_criteria, \
    default_criteria_messages = _handle_default_criteria(
        default_criteria,
        participant
    )

    invalid_specific_criteria, \
    specific_criteria_messages = _handle_specific_criteria(
        experiment,
        data,
        participant
    )

    invalid_previous_experiments, \
    experiment_messages = _handle_excluded_experiments(
        experiment,
        participant
    )

    invalid_misc_items, \
    misc_messages = _handle_misc_items(
        data,
        time_slot,
    )

    success = not invalid_default_criteria and not invalid_specific_criteria \
              and not invalid_previous_experiments and not invalid_misc_items

    if success:
        # Save this participant, make the appointment and register any
        # answers to specific criteria we didn't know yet
        participant.save()
        _make_appointment(participant, time_slot)
        _add_specific_criteria_answers(participant, experiment, data)

        # We set recoverable to false, as there is nothing to recover
        # Also, it's easier to work with in the client's view
        return success, False, ["Je bent ingeschreven voor het experiment! "
                                "Je krijgt een bevestiging per email."]

    recoverable = not invalid_default_criteria and not \
        invalid_specific_criteria and not invalid_previous_experiments

    # Else, get human-friendly messages and return the whole thing
    messages = _format_messages(
        default_criteria_messages,
        specific_criteria_messages,
        experiment_messages,
        misc_messages,
    )

    # Success, recoverable, messages
    return success, recoverable, messages


def get_required_fields(experiment: Experiment, participant: Participant):
    fields = ['name', 'phone', 'social_status']

    for field in experiment.defaultcriteria.__dict__.keys():
        if field not in ['experiment', 'experiment_id', 'min_age', 'max_age',
                         'dyslexia', '_state', 'social_status']:
            if getattr(participant, field) is None:
                fields.append(field)

    if getattr(participant, 'birth_date') is None:
        fields.append('birth_date')

    if participant.dyslexic is None:
        fields.append('dyslexia')

    # All specific criteria should be answered, even if we already have the
    # answer. The answer to SC can change (like 'has lived in A'dam in the
    # last x years)
    for experiment_criterion in experiment.experimentcriterion_set.all():
        fields.append(experiment_criterion.criterion.name_form)

    return fields


def _get_participant(data: dict) -> Participant:
    email = data.get('email').strip()
    participants = Participant.objects.find_by_email(email)

    # If we have a participant, get the first one that matches
    if len(participants) > 0:
        participant = participants[0]
    else:
        # If not, create a new one
        participant = Participant()
        participant.email = email

    # These variables aren't allowed to be changed by the participant
    # (And most shouldn't be able to change irl, unless a cure for
    # dyslexia has been developed. In which case, please do tell)
    # However, we might not know them yet. x_or_else will keep the existing
    # data, but if the existing data is None it will update with the given data.
    participant.name = x_or_else(
        participant.name,
        data.get('name')
    )

    participant.multilingual = x_or_else(
        participant.multilingual,
        data.get('multilingual') == 'Y'
    )

    participant.language = x_or_else(
        participant.language,
        data.get('language')
    )

    participant.handedness = x_or_else(
        participant.handedness,
        data.get('handedness')
    )

    participant.sex = x_or_else(
        participant.sex,
        data.get('sex')
    )

    if data.get('birth_date'):
        participant.birth_date = x_or_else(
            participant.birth_date,
            parse_date(data.get('birth_date'))
        )

    participant.dyslexic = x_or_else(
        participant.dyslexic,
        data.get('dyslexic') == 'Y'
    )

    # Update/set all variables that can be changed
    # But only if provided
    participant.social_status = x_or_else(
        data.get('social_status', None),
        participant.social_status
    )

    participant.phonenumber = x_or_else(
        data.get('phone', None),
        participant.phonenumber
    )

    if 'mailinglist' in data:
        participant.email_subscription = data.get('mailinglist')

    return participant

def _handle_default_criteria(
        default_criteria: DefaultCriteria,
        participant: Participant,
) -> Tuple[list, list]:
    messages = []

    filters = build_exclusion_filters(default_criteria)
    failed_criteria = check_default_criteria(participant, filters)

    for failed_criterion in failed_criteria:

        # These fields have different error messages depending on the
        # expected value
        if failed_criterion in ['multilingual', 'dyslexic', 'social_status']:

            # Map booleans to yes,no
            if isinstance(filters[failed_criterion], bool):
                if filters[failed_criterion]:
                    specifier = 'yes'
                else:
                    specifier = 'no'
            else:
                # Otherwise, just use the value0
                specifier = filters[failed_criterion]

            # Make the right key
            message_key = "{}_{}".format(failed_criterion, specifier)

            messages.append(
                DEFAULT_INVALID_MESSAGES[message_key]
            )
        else:
            messages.append(DEFAULT_INVALID_MESSAGES[failed_criterion])

    if should_exclude_by_age(participant, default_criteria):
        failed_criteria.append('age')
        messages.append(DEFAULT_INVALID_MESSAGES['age'])

    return failed_criteria, messages


def _handle_specific_criteria(
        experiment: Experiment,
        data: dict,
        participant: Participant
) -> Tuple[list, list]:
    """
    Warning! This method does not lean on anything in exclusion.py, as it's data
    source is fundamentally different.

    _should_exclude_by_specific_criteria in exclusion.py uses Django's data
    layer, this method uses API data in dict form.

    :param experiment:
    :param data:
    :param participant:
    :return:
    """
    specific_criteria = experiment.experimentcriterion_set.all()
    failed_criteria = []
    messages = []

    # Check if we have specific criteria in our data, if not: fail all fields
    if 'specific_criteria' not in data or not data['specific_criteria']:
        if 'full' in data and data['full']:
            for specific_criterion in specific_criteria:
                failed_criteria.append(specific_criterion.criterion.name_form)
                messages.append(specific_criterion.message_failed)

            return failed_criteria, messages

        full_form = False
    else:
        full_form = True
        try:
            # Rewrite the list of dicts back into a dict of field: value
            data = {x['name']: int(x['value']) for x in
                    data['specific_criteria']}
        except ValueError:
            # ValueError means the user is submitting weird data. This should
            # not happen, but just in case we are going to crash Django in a
            # secure manner
            raise SuspiciousOperation

    for specific_criterion in specific_criteria:
        name_form = specific_criterion.criterion.name_form

        if name_form not in data and full_form:
            failed_criteria.append(
                name_form
            )
            messages.append(specific_criterion.message_failed)
            continue

        existing_answer = participant.criterionanswer_set.filter(
            criterion=specific_criterion.criterion
        ).first()

        value = data.get(name_form, None)

        # If we have a value from the form, use that one
        if value is not None:
            # The value sent is actually an integer index corresponding to a
            # value in values_list, so we extract the chosen value from that
            # list.
            value = specific_criterion.criterion.values_list[value]
        elif existing_answer and not full_form:
            # If this is not a full-form processing and we have an existing
            # answer, use that one.
            value = existing_answer.answer

        if specific_criterion.correct_value != value:
            failed_criteria.append(name_form)
            messages.append(specific_criterion.message_failed)

        if existing_answer:
            # Check if the value answered conflicts with the answer this
            # participant has already given (if that previous answer exists)
            # (Note: this will always fail if we are in fact using an
            # existing answer. Not that it matters)
            if value and existing_answer.answer != value:
                # Make a comment informing the admins for this situation.
                # We are not going to fail this directly, as some criteria
                # answers can actually change over time. (For example: has
                # lived in Utrecht in the past month).
                comment = "Gave a different answer to a criteria " \
                          "he/she answered before: {}, old answer: " \
                          "{}, new answer: {}"
                comment = comment.format(
                    specific_criterion.criterion.name_natural,
                    existing_answer.answer,
                    value
                )

                add_system_comment(participant, comment, experiment)

                existing_answer.answer = value
                existing_answer.save()

    return failed_criteria, messages


def _handle_excluded_experiments(
        experiment: Experiment,
        participant: Participant
) -> Tuple[List[Experiment], List[str]]:
    """
    Warning! This method does not lean on anything in exclusion.py, as the
    exclusion.py version does this with complicated SQL for better performance.
    (As that method processes ALL participants)

    :param experiment:
    :param data:
    :param participant:
    :return:
    """
    invalid_experiments = []
    appointments = participant.appointments.all()
    participated_experiments = [x.timeslot.experiment for x in appointments]

    for excluded_experiment in experiment.excluded_experiments.all():
        if excluded_experiment in participated_experiments:
            invalid_experiments.append(excluded_experiment)

    messages = []
    if invalid_experiments:
        messages = [
            MISC_INVALID_MESSAGES['invalid_experiment']
        ]

    return invalid_experiments, messages


def _handle_misc_items(data: dict, time_slot: TimeSlot) -> Tuple[list, list]:
    invalid_fields = []
    messages = []

    # Check if the timeslot is still free
    if not time_slot or not time_slot.has_free_places():
        invalid_fields.append('timeslot')
        messages.append(MISC_INVALID_MESSAGES['timeslot'])

    # Ensure this is a valid email address
    try:
        validate_email(data.get('email'))
    except ValidationError:
        invalid_fields.append('email')
        messages.append(MISC_INVALID_MESSAGES['email'])

    return invalid_fields, messages


def _make_appointment(participant: Participant, time_slot: TimeSlot) -> None:
    appointment = Appointment()
    appointment.participant = participant
    appointment.timeslot = time_slot
    appointment.save()

    admin = get_supreme_admin()
    experiment = appointment.timeslot.experiment

    subject = 'Bevestiging afspraak experiment UiL OTS: {}'.format(
        experiment.name
    )

    cancel_link = parse.urljoin(settings.FRONTEND_URI, 'participant/cancel/')

    context = {
        'participant': participant,
        'time_slot':   time_slot,
        'experiment':  experiment,
        'leader':      experiment.leader,
        'cancel_link': cancel_link
    }

    send_template_email(
        [participant.email],
        subject,
        'api/mail/new_appointment',
        context,
        admin.email
    )


def _add_specific_criteria_answers(participant: Participant, experiment:
Experiment, data: dict) -> None:
    specific_criteria = experiment.experimentcriterion_set.all()

    try:
        # Rewrite the list of dicts back into a dict of field: value
        data = {x['name']: int(x['value']) for x in data['specific_criteria']}
    except ValueError:
        # ValueError means the user is submitting weird data. This should not
        # happen, but just in case we are going to crash Django in a secure
        # manner
        raise SuspiciousOperation

    for specific_criterion in specific_criteria:
        name_form = specific_criterion.criterion.name_form

        if name_form not in data:
            continue

        # Check if we have an existing answer. If so, we are going to ignore
        # this criterion
        answer_exists = participant.criterionanswer_set.filter(
            criterion=specific_criterion.criterion
        ).exists()

        if not answer_exists:
            value = data.get(name_form)
            # The value sent is actually an integer index corresponding to a
            # value in values_list, so we extract the chosen value from that
            # list.
            value = specific_criterion.criterion.values_list[value]

            answer = CriterionAnswer()
            answer.participant = participant
            answer.criterion = specific_criterion.criterion
            answer.answer = value

            answer.save()


def _format_messages(*messages: List[str]) -> list:
    # Flatten the list of lists
    messages = [item for sublist in messages for item in sublist]

    return [_format_message(message) for message in messages]

def _format_message(message: str) -> str:
    admin = get_supreme_admin()
    contact_string = '<a href="mailto:{}">{}</a>'.format(
        admin.email,
        admin.get_full_name()
    )

    return message.format(contact_string)
