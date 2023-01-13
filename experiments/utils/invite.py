from typing import List
import urllib.parse as parse

from django.conf import settings
from django.core.mail import get_connection

from experiments.emails import DEFAULT_INVITE_FOOTER, InviteEmail
from experiments.models import Experiment, Invitation
from main.utils import get_supreme_admin, get_register_link
from participants.models import Participant
from participants.utils import get_mailinglist_unsubscribe_url


def get_initial_invite_context(experiment: Experiment) -> dict:
    context = {
        'duration':                experiment.duration,
        'compensation':            experiment.compensation,
        'task_description':        experiment.task_description,
        'additional_instructions': experiment.additional_instructions,
        'experiment_name':         experiment.name,
        'experiment_location':     '',
        'leader_name':             experiment.leader.name,
        'leader_email':            experiment.leader.api_user.email,
        'leader_phonenumber':      experiment.leader.phonenumber,
        'all_leaders_name_list':   experiment.all_leaders_str,
        'admin':                   get_supreme_admin().get_full_name(),
        'reg_through_login_link':  _get_login_exp_url(experiment),
        'reg_link':                get_register_link(experiment),
    }

    if experiment.location:
        context['experiment_location'] = experiment.location.name

    return context


def mail_invite(
        participant_ids: List[str],
        content: str,
        experiment: Experiment) -> None:
    context = get_initial_invite_context(experiment)

    connection = get_connection()

    email = InviteEmail(
        to='',
        contents=content,
        subject='ILS Labs uitnodiging deelname experiment: {}'.format(
            experiment.name
        ),
    )

    participants = Participant.objects.filter(pk__in=participant_ids)
    participants.prefetch_related()

    for participant in participants:
        part_context = {
            'name': participant.mail_name,
            'participant': participant,
            'unsub_link': get_mailinglist_unsubscribe_url(participant)
        }
        part_context.update(context)

        if participant.api_user:
            email.footer = "<p>Tip! Gebruik <a href=\"{{ " \
                           "reg_through_login_link }}\" " \
                           "style=\"color:#fff;\">deze  link</a> om in " \
                           "te loggen en dan direct naar de inschrijf pagina " \
                           "te gaan! Indien je ingelogt bent hoef je niet " \
                           "alle gegevens meer in te vullen die wij al " \
                           "hebben.</p>" + DEFAULT_INVITE_FOOTER
        else:
            email.footer = DEFAULT_INVITE_FOOTER

        email.context = part_context
        email.to = [participant.email]
        email.send(connection=connection)

    # Create a new invitation object for all participants, so we see a nice
    # checkbox
    Invitation.objects.bulk_create(
        [Invitation(experiment=experiment, participant=participant) for
         participant in participants if participant]
    )


def _get_login_exp_url(experiment: Experiment) -> str:
    return parse.urljoin(
        settings.FRONTEND_URI,
        "login/?next=/participant/register/{}/".format(
            experiment.pk,
        )
    )
