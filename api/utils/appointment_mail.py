from django.conf import settings
from django.template import defaultfilters
from django.utils.timezone import localtime
import urllib.parse as parse

from experiments.emails import ConfirmationEmail

from experiments.models import Experiment, TimeSlot
from participants.models import Participant

CANCEL_LINK_REGEX = r'{cancel_link(?::\"(.*)\")?}'


def get_initial_confirmation_context(experiment: Experiment) -> dict:
    context = {
        'experiment_name': experiment.name,
        'experiment_location': '',
        'leader_name': experiment.leader.name,
        'leader_email': experiment.leader.api_user.email,
        'leader_phonenumber': experiment.leader.phonenumber,
        'all_leaders_name_list': experiment.all_leaders_str,
        'cancel_link': parse.urljoin(
            settings.FRONTEND_URI,
            'participant/cancel/'
        ),
    }

    if experiment.location:
        context['experiment_location'] = experiment.location.name

    return context


def send_appointment_mail(
        experiment: Experiment,
        participant: Participant,
        time_slot: TimeSlot,
) -> None:

    # Should not happen, but as that field technically now can be none we make
    # sure to handle it.
    if participant.email is None:
        return

    context = get_initial_confirmation_context(experiment)
    context.update({
        'name': participant.mail_name,
    })

    if experiment.use_timeslots:
        # We don't use strftime because that's not _always_ timezone aware
        # Also, using the template filter is a neat hack to have the same format
        # string syntax everywhere
        context.update({
            'date': defaultfilters.date(localtime(time_slot.datetime), 'l d-m-Y'),
            'time': defaultfilters.date(localtime(time_slot.datetime), 'H:i'),
        })

    email = ConfirmationEmail(
        to=[participant.email],
        subject='Bevestiging inschrijving experiment UiL OTS: {}'.format(
            experiment.name
        ),
        contents=experiment.confirmation_email,
        context=context,
    )
    email.send()

