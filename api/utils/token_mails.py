from typing import Tuple
import urllib.parse as parse

from django.conf import settings
from cdh.mail.utils import send_template_email

from api.auth.models import ApiUser
from participants.models import Participant


def send_password_reset_mail(user: ApiUser, token: str) -> None:
    link, alternative_link = get_reset_links(token)

    subject = 'ILS Labs Experimenten: password reset'
    context = {
        'token':            token,
        'name':             _get_name(user),
        'link':             link,
        'alternative_link': alternative_link,
    }

    send_template_email(
        [user.email],
        subject,
        html_template='api/mail/password_reset.html',
        plain_template='api/mail/password_reset.txt',
        template_context=context,
    )


def send_cancel_token_mail(participant: Participant, token: str,
                           email: str) -> None:
    link = parse.urljoin(
        settings.FRONTEND_URI,
        "participant/appointments/{}/".format(token)
    )

    subject = 'ILS Labs Experimenten: afspraak afzeggen'
    context = {
        'token': token,
        'name':  participant.name or 'proefpersoon',
        'link':  link,
    }

    send_template_email(
        [email],
        subject,
        html_template='api/mail/cancel_token.html',
        plain_template='api/mail/cancel_token.txt',
        template_context=context,
    )


def _get_name(user: ApiUser) -> str:
    if hasattr(user, 'participant'):
        return user.participant.mail_name

    if hasattr(user, 'leader'):
        return user.leader.name

    return 'proefpersoon'


def get_reset_links(token: str) -> Tuple[str, str]:
    if not isinstance(token, str):
        token = str(token)

    root = parse.urljoin(
        settings.FRONTEND_URI,
        "reset_password/"
    )

    complete = parse.urljoin(
        root,
        token + "/"
    )

    return complete, root
