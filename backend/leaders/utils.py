from datetime import datetime, timedelta
import urllib.parse as parse
from enum import Enum
from typing import Optional

from django.conf import settings
from pytz import timezone
from cdh.mail.utils import send_template_email

from api.auth.ldap_backend import ApiLdapBackend
from api.auth.models import ApiGroup, ApiUser, UserToken
from api.utils import get_reset_links
from main.utils import is_ldap_enabled
from .models import Leader


def create_leader(name: str, email: str, phonenumber: str,
                  password: str = None) -> (Leader, bool):
    """
    This function creates a new Leader object.

    If the email specified is already used, it will return the Leader object for
    that email.

    If there already is a ApiUser object with that email, that one will be
    retrieved and used in the Leader object. This can happen if someone who
    already made an account as a participant is added as a leader.

    If no ApiUser object exists, one will be created.

    In both cases the ApiUser object is added to the leader group.

    :param name:
    :param email:
    :param phonenumber:
    :param password:
    :return:
    """
    _leader_group = ApiGroup.objects.get(name=settings.LEADER_GROUP)
    existing_leader = Leader.objects.filter(api_user__email=email)

    if existing_leader:
        return existing_leader[0], True

    leader = Leader()
    leader.name = name
    leader.phonenumber = phonenumber

    existing_api_user = ApiUser.objects.get_by_email(email)
    existing = False

    if existing_api_user:
        existing = True
        api_user = existing_api_user
    else:
        api_user = ApiUser()
        api_user.email = email

        if password:
            api_user.set_password(password)
            api_user.passwords_needs_change = True

        api_user.save()

    if _leader_group not in api_user.groups.all():
        api_user.groups.add(_leader_group)
        api_user.save()

    leader.api_user = api_user
    leader.save()

    return leader, existing


def create_ldap_leader(name: str, email: str, phonenumber: str) -> \
        Optional[Leader]:
    """
    This function creates a new Leader object, which will log in through the
    LDAP.

    If the email specified is already used, it will return the Leader object for
    that email.

    If there already is a ApiUser object with that email, that one will be
    retrieved and used in the Leader object. That account will NOT be
    updated to use ldap. This can happen if someone who already made an account
     as a participant is added as a leader.

    If no ApiUser object exists, one will be created.

    In both cases the ApiUser object is added to the leader group.

    :param email:
    :return:
    """
    _leader_group = ApiGroup.objects.get(name=settings.LEADER_GROUP)
    existing_leader = Leader.objects.filter(api_user__email=email)

    if existing_leader:
        return existing_leader[0]

    leader = Leader()
    leader.name = name
    leader.phonenumber = phonenumber

    existing_api_user = ApiUser.objects.get_by_email(email)

    if existing_api_user:
        api_user = existing_api_user
        pre_population_user = None  # Keeps the linter happy
    else:
        # Create an empty account first, before we populate
        pre_population_user = ApiUser.objects.create(email=email)
        api_user = ApiLdapBackend().populate_user(email)

    if not api_user:
        # Clean up if population didn't work
        if pre_population_user:
            pre_population_user.delete()
        return None

    if _leader_group not in api_user.groups.all():
        api_user.groups.add(_leader_group)
        api_user.save()

    leader.api_user = api_user
    leader.save()

    return leader


def get_login_link() -> str:
    return parse.urljoin(
        settings.FRONTEND_URI,
        "login/"
    )


def notify_new_leader(leader: Leader, existing=False) -> None:
    has_password = leader.api_user.has_password

    template = 'leaders/mail/notify_new_leader'
    if existing:
        template = 'leaders/mail/notify_new_leader_existing_account'

    if not has_password:
        token_model = UserToken.objects.create(
            user=leader.api_user,
            expiration=_get_tomorrow(),
            type=UserToken.PASSWORD_RESET,
        )
        token = token_model.token

        link, alternative_link = get_reset_links(token_model.token)
    else:
        token = None
        link = None
        alternative_link = None

    subject = 'ILS Labs Experimenten: new account'
    context = {
        'has_password':     has_password,
        'token':            token,
        'name':             leader.name,
        'email':            leader.api_user.email,
        'link':             link,
        'alternative_link': alternative_link,
        'login_link':       get_login_link(),
    }

    send_template_email(
        [leader.api_user.email],
        subject,
        html_template=f"{template}.html",
        plain_template=f"{template}.html",
        template_context=context,
    )


def notify_new_ldap_leader(leader: Leader) -> None:
    subject = 'ILS Labs Experimenten: new account'
    context = {
        'name':             leader.name,
        'email':            leader.api_user.email,
        'login_link':       get_login_link(),
    }

    send_template_email(
        [leader.api_user.email],
        subject,
        html_template='leaders/mail/notify_new_ldap_leader.html',
        plain_template='leaders/mail/notify_new_ldap_leader.txt',
        template_context=context,
    )


def _get_tomorrow():
    tz = timezone(settings.TIME_ZONE)
    return datetime.now(tz) + timedelta(hours=24)


def update_leader(leader: Leader, name: str, email: str, phonenumber: str,
                  password: str = None, is_active: bool = True) -> Leader:
    _leader_group = ApiGroup.objects.get(name=settings.LEADER_GROUP)
    _participant_group = ApiGroup.objects.get(name=settings.PARTICIPANT_GROUP)

    leader.name = name
    leader.phonenumber = phonenumber
    leader.save()

    api_user = leader.api_user
    api_user.email = email

    if is_active:
        if _leader_group not in api_user.groups.all():
            api_user.groups.add(_leader_group)

        api_user.is_active = True
    else:
        if _leader_group in api_user.groups.all():
            api_user.groups.remove(_leader_group)

        # The account should still be active if the leader is also a participant
        api_user.is_active = _participant_group in api_user.groups.all()

    if password:
        api_user.passwords_needs_change = True
        api_user.set_password(password)

    api_user.save()

    return leader


def delete_leader(leader: Leader) -> None:
    _leader_group = ApiGroup.objects.get(name=settings.LEADER_GROUP)
    _participant_group = ApiGroup.objects.get(name=settings.PARTICIPANT_GROUP)

    api_user = leader.api_user

    all_groups = api_user.groups.all()

    if _leader_group in all_groups:
        if len(all_groups) == 1:
            api_user.delete()
        else:
            api_user.groups.remove(_leader_group)
            api_user.is_active = _participant_group in all_groups

            api_user.is_ldap_account = False

            api_user.save()

    leader.delete()


class ConvertResult(Enum):
    NO_OP = "NO_OP"
    INVALID_EMAIL = "INVALID_EMAIL"
    UNKNOWN_USER = "UNKNOWN_USER"
    SUCCESS = "SUCCESS"


def convert_leader_to_ldap(leader: Leader) -> ConvertResult:
    """All hail the mighty LDAP!
    Oh wait, it's not that kind of conversion... bummer

    Changes an eligible non-ldap-enabled leader account to use ldap for
    authentication
    """
    api_user = leader.api_user

    if not is_ldap_enabled() or api_user.is_ldap_account:
        return ConvertResult.NO_OP

    if not api_user.email.endswith("uu.nl"):
        return ConvertResult.INVALID_EMAIL

    api_user.set_password(None)
    api_user.passwords_needs_change = False
    api_user.save()

    user = ApiLdapBackend().populate_user(api_user.email)

    if user:
        user.is_ldap_account = True
        user.save()
        return ConvertResult.SUCCESS

    return ConvertResult.UNKNOWN_USER
