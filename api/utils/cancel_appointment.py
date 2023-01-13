from datetime import datetime, timedelta

from django.conf import settings
from cdh.core.mail.utils import send_template_email

from comments.utils import add_system_comment
from experiments.models import Appointment
from main.utils import get_supreme_admin, get_register_link
from participants.utils import get_mailinglist_unsubscribe_url


def cancel_appointment(appointment: Appointment) -> None:
    # Only handle late comment if there is a timeslot
    if appointment.timeslot:
        _handle_late_comment(appointment)
    _inform_leaders(appointment)
    _send_confirmation(appointment)

    appointment.delete()


def _handle_late_comment(appointment: Appointment) -> None:
    """Helper function that adds a comment for this participant if he/she/it
    cancelled within 24 prior to the appointment.
    """
    dt = appointment.timeslot.datetime

    now = datetime.now(tz=dt.tzinfo)

    deadline = dt - timedelta(days=1)

    if now > deadline:
        add_system_comment(
            appointment.participant,
            "Cancelled less than 24h before experiment",
            appointment.timeslot.experiment
        )


def _inform_leaders(appointment: Appointment) -> None:
    experiment = appointment.experiment

    leaders = [experiment.leader]
    if experiment.additional_leaders.exists():
        leaders.extend(experiment.additional_leaders.all())

    for leader in leaders:
        subject = 'ILS Labs participant deregistered for experiment: {}'.format(
            experiment.name)
        context = {
            'participant': appointment.participant,
            'time_slot':   appointment.timeslot,
            'experiment':  experiment,
            'leader':      leader,
        }

        send_template_email(
            [leader.email],
            subject,
            html_template='api/mail/participant_cancelled.html',
            plain_template='api/mail/participant_cancelled.txt',
            template_context=context,
        )


def _send_confirmation(appointment: Appointment) -> None:

    # Should not happen, but as that field technically now can be none we make
    # sure to handle it.
    if appointment.participant.email is None:
        return

    admin = get_supreme_admin()
    experiment = appointment.experiment
    time_slot = appointment.timeslot

    subject = 'ILS Labs uitschrijven experiment: {}'.format(experiment.name)
    context = {
        'participant':             appointment.participant,
        'time_slot':               time_slot,
        'experiment':              experiment,
        'admin':                   admin.get_full_name(),
        'admin_email':             admin.email,
        'other_time_link':         get_register_link(experiment),
        'home_link':               settings.FRONTEND_URI,
        'mailinglist_unsubscribe': get_mailinglist_unsubscribe_url(
            appointment.participant
        )
    }

    send_template_email(
        [appointment.participant.email],
        subject,
        html_template='api/mail/cancelled_appointment.html',
        plain_template='api/mail/cancelled_appointment.txt',
        template_context=context,
    )
