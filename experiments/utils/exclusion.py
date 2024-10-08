"""
Note: the functions in this module are heavily optimised to minimize
processing and database accesses. This does mean that the code is not as
straightforward as you'd expect.

Also, because we use application-level database encryption, we cannot compare
inside the database. This is why everything is done in python.
"""
import datetime
from typing import List, Optional
from django.db.models.expressions import RawSQL

from experiments.models import Experiment, ExperimentCriterion
from experiments.models.criteria_models import DefaultCriteria
from participants.models import CriterionAnswer, Participant

# List of vars that can have the same values as the participant model
# variables, with an indifferent option
indifferentable_vars = [
    'language',
    'sex',
    'handedness',
    'social_status',
]


def get_eligible_participants_for_experiment(experiment: Experiment,
                                             on_mailinglist: bool = True) -> \
        List[Participant]:
    """
    This function produces a list of participants that can take part in
    the provided experiment.
    """
    default_criteria = experiment.defaultcriteria
    specific_experiment_criteria = \
        experiment.experimentcriterion_set.select_related(
            'criterion'
        )

    # Base filters: a participant should be capable, and by default be on the
    # mailing list
    filters = {
        'email_subscription': on_mailinglist,
        'capable':            True,
    }

    # Build the rest of the filters
    filters = build_exclusion_filters(default_criteria, filters)

    # Exclude all participants with an appointment for an experiment that was
    # marked as an exclusion criteria
    participants = Participant.objects.exclude(
        appointments__experiment__in=experiment.excluded_experiments.all()
    ).exclude(
        # Exclude all participants who have already signed up
        appointments__experiment=experiment
    ).prefetch_related(
        'secondaryemail_set',  # Used in the invite page template!
        'criterionanswer_set'
    )

    # List of all allowed participants
    filtered = []

    for participant in participants:

        # If we don't have a primary email we can't really invite them, so skip!
        if participant.email is None:
            continue

        if check_default_criteria(participant, filters):
            continue

        if should_exclude_by_age(participant, default_criteria):
            continue

        if _should_exclude_by_specific_criteria(participant,
                                                specific_experiment_criteria):
            continue

        filtered.append(participant)

    return filtered


def check_participant_eligible(experiment: Experiment, participant:
Participant) -> bool:
    """
    This function checks if a given participant can participate in a given
    experiment
    """

    default_criteria = experiment.defaultcriteria
    specific_experiment_criteria = \
        experiment.experimentcriterion_set.select_related(
            'criterion'
        )

    filters = build_exclusion_filters(default_criteria)

    if check_default_criteria(participant, filters):
        return False

    if should_exclude_by_age(participant, default_criteria):
        return False

    if _should_exclude_by_specific_criteria(participant,
                                            specific_experiment_criteria):
        return False

    return True


def build_exclusion_filters(default_criteria, filters=None) -> dict:
    """
    This function expands a given filter dict with filters as specified in
    the given default_criteria
    :param filters:
    :param default_criteria:
    :return:
    """
    if filters is None:
        filters = {}

    for var in indifferentable_vars:
        if getattr(default_criteria, var) != 'I':
            filters[var] = getattr(default_criteria, var)

    # Rewrite this expected to a boolean value, as it's stored as a boolean
    if default_criteria.dyslexia != 'I':
        expected_value = default_criteria.dyslexia == 'Y'
        filters['dyslexic'] = expected_value

    # Rewrite this expected to a boolean value, as it's stored as a boolean
    if default_criteria.multilingual != 'I':
        expected_value = default_criteria.multilingual == 'Y'
        filters['multilingual'] = expected_value

    return filters


def check_default_criteria(participant: Participant, filters: dict) -> list:
    """
    Determines if a participant should be excluded based upon a given filter
    dict
    :param participant:
    :param filters:
    :return:
    """
    failed_criteria = []

    # Loop over the defined filters
    for attr, expected_value in filters.items():
        found_value = getattr(participant, attr, None)
        # If we the found value is not the same as the expected,
        # mark this participant as 'to exclude'. None means we don't have this
        # value, so we give it the benifit of the doubt and allow it anyways
        if found_value != expected_value and found_value is not None:
            failed_criteria.append(attr)

    return failed_criteria


def _should_exclude_by_specific_criteria(participant: Participant,
                                         specific_experiment_criteria) -> bool:
    """
    Determines if a participant should be excluded based upon their
    :param participant:
    :param specific_experiment_criteria:
    :return:
    """
    # Create a list of all relevant Criterion objects
    specific_criteria = [x.criterion for x in specific_experiment_criteria]

    # Loop over all criteria answers
    for specific_criterion_answer in participant.criterionanswer_set.all():
        # Check if this answer is for any of the relevant criterions
        # We do this in python to minimize db queries (it's way faster)
        if specific_criterion_answer.criterion not in specific_criteria:
            continue

        # Get the experiment criterion
        specific_criterion = _get_specific_criterion(
            specific_experiment_criteria,
            specific_criterion_answer.criterion
        )

        if specific_criterion and not specific_criterion_answer.answer == \
                                      specific_criterion.correct_value:
            return True

    return False


def _get_specific_criterion(specific_experiment_criteria, criterion) -> \
        ExperimentCriterion:
    """
    Gets the experimentCriterion object for a criterion object
    :param specific_experiment_criteria:
    :param criterion:
    :return:
    """
    for x in specific_experiment_criteria:
        if x.criterion == criterion:
            return x


def should_exclude_by_age(participant: Participant, default_criteria: DefaultCriteria,
                          appointment_date: Optional[datetime.date]=None) -> bool:
    """
    Determines if a participant should be excluded based upon their age

    :param participant:
    :param default_criteria:
    :return:
    """
    age = participant.age_at(appointment_date) if appointment_date else participant.age

    # If we don't know the age, assume it's allowed
    if age is None:
        return False

    if age < default_criteria.min_age:
        return True

    max_age = default_criteria.max_age
    if max_age == -1:  # no max
        return False

    return age > max_age
