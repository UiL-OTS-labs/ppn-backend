import urllib.parse as parse

from django.conf import settings
from django.template import defaultfilters
from django.utils import translation
from django.utils.timezone import localtime

from cdh.core.utils.mail import send_template_email
from experiments.emails import ReminderEmail

from experiments.models import Appointment, Experiment, TimeSlot
from main.utils import get_supreme_admin
from participants.models import Participant


def get_initial_reminder_context(experiment: Experiment) -> dict:
    context = {
        'experiment_name': experiment.name,
        'experiment_location': '',
        'leader_name': experiment.leader.name,
        'leader_email': experiment.leader.api_user.email,
        'leader_phonenumber': experiment.leader.phonenumber,
        'all_leaders_name_list': experiment.all_leaders_str,
        'admin': get_supreme_admin().get_full_name(),
        'cancel_link': parse.urljoin(
            settings.FRONTEND_URI,
            'participant/cancel/'
        ),
    }

    # TODO: custom cancel link?

    if experiment.location:
        context['experiment_location'] = experiment.location.name

    return context


def send_reminder_mail(
    appointment: Appointment
) -> None:
    experiment = appointment.experiment
    participant = appointment.participant
    timeslot = None

    if experiment.use_timeslots:
        timeslot = appointment.timeslot

    context = get_initial_reminder_context(experiment)
    context.update({
        'name': participant.mail_name,
    })

    if timeslot:
        # We don't use strftime because that's not _always_ timezone aware
        # Also, using the template filter is a neat hack to have the same format
        # string syntax everywhere
        old_lang = translation.get_language()
        translation.activate('nl')
        context.update({
            'date': defaultfilters.date(localtime(timeslot.datetime), 'l d-m-Y'),
            'time': defaultfilters.date(localtime(timeslot.datetime), 'H:i'),
        })
        translation.activate(old_lang)

    email = ReminderEmail(
        to=[participant.email],
        subject='*Reminder* opgave experiment: {}'.format(experiment.name),
        contents=experiment.reminder_email,
        context=context,
    )
    email.send()


def _make_cancel_link() -> str:
    return parse.urljoin(
        settings.FRONTEND_URI,
        "participant/cancel/"
    )
