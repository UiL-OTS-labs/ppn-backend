from datetime import datetime

from typing import List, Tuple

from experiments.models import Appointment
from datamanagement.utils.common import get_threshold_years_ago
from participants.models import Participant
from auditlog.utils.log import log as log_to_auditlog
from auditlog.enums import Event, UserType
from django.db.models import Count, Max


def get_participants_with_appointments() -> List[Tuple[Participant, datetime, int]]:
    out = []
    threshold = get_threshold_years_ago("participants_with_appointment")

    for pp in (
        Participant.objects.filter(anonymized=False)
        .annotate(
            last=Max("appointments__timeslot__datetime"),
            count=Count("appointments__id"),
        )
        .filter(last__lte=threshold)
    ):
        out.append((pp, pp.last, pp.count))

    return out


def get_participants_without_appointments() -> List[Participant]:
    return list(
        Participant.objects.filter(
            appointments=None,
            created__lte=get_threshold_years_ago("participants_without_appointment"),
            anonymized=False,
        )
    )


def delete_participant(participant: Participant, user) -> bool:
    if participant not in get_participants_without_appointments():
        return False

    log_to_auditlog(
        Event.DELETE_DATA,
        "Deleted participant '{}'".format(participant),
        user,
        UserType.ADMIN,
    )

    # Delete the account as well, unless the account is also a leader
    if participant.api_user and not participant.api_user.leader:
        participant.api_user.delete()

    participant.delete()

    return True


def anonymize_participant(participant: Participant, user) -> None:
    log_to_auditlog(
        Event.MODIFY_DATA,
        "Anonymized participant '{}'".format(participant),
        user,
        UserType.ADMIN,
    )
    participant.anonymize()
