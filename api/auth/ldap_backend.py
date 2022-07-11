from django_auth_ldap.backend import _LDAPUser, logger

from api.auth.models import ApiUser
from main.auth import PpnLdapBackend


class ApiLdapBackend(PpnLdapBackend):
    settings_prefix = "AUTH_LDAP_API_"

    def get_user_model(self):
        return ApiUser

    def authenticate(
            self,
            username=None,
            password=None,
            stop_recursion=False,
            **kwargs
    ):
        if password or self.settings.PERMIT_EMPTY_PASSWORD:
            ldap_user = _LDAPUser(self, username=username.strip())
            user = self.authenticate_ldap_user(ldap_user, password)
        else:
            logger.debug('Rejecting empty password for {}'.format(username))
            return None

        # Make sure people can still login even if they use the wrong email
        if not user and not stop_recursion and username.endswith(
                '@students.uu.nl'
        ):
            username = username.replace('students.uu.nl', 'uu.nl')
            user = self.authenticate(username, password, True, **kwargs)
        elif not user and not stop_recursion and username.endswith('@uu.nl'):
            username = username.replace('uu.nl', 'students.uu.nl')
            user = self.authenticate(username, password, True, **kwargs)

        return user

    def _get_user_object(self,
                         model,
                         lookup: str,
                         query_value: str):
        try:
            user = model.objects.get_by_email(**{
                lookup: query_value
            })
        except model.DoesNotExist:
            user = None

        return user
