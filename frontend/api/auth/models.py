from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db import models

from api.auth.exceptions import AccountAlreadyExistsException
from api.resources.account_resources import UserCreationData


class RemoteApiUserManager(BaseUserManager):

    def create_user(self,
                    email: str,
                    name: str,
                    multilingual: bool = None,
                    language: str = None,
                    dyslexic: bool = None,
                    mailing_list: bool = False,
                    password: str = None,
                    **kwargs):

        resource = UserCreationData(
            email=email,
            name=name,
            multilingual=multilingual,
            language=language,
            dyslexic=dyslexic,
            mailing_list=mailing_list,
            password=password,
        )

        response = resource.put()

        if response.message and response.message != 'OK':
            if response.message == 'ACCOUNT_ALREADY_EXISTS':
                raise AccountAlreadyExistsException

    def create_superuser(self, *args, **kwargs):
        raise RuntimeError("Admin User generation is not supported in this "
                           "application. Create users in the backend!")


class RemoteApiUser(PermissionsMixin, AbstractBaseUser):
    objects = RemoteApiUserManager()

    remote_id = models.IntegerField(null=False, blank=False, unique=True)

    USERNAME_FIELD = 'remote_id'
    EMAIL_FIELD = None

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_ldap_account = models.BooleanField(default=False)

    @property
    def is_leader(self) -> bool:
        return self.groups.filter(name=settings.GROUPS_LEADER).exists()

    @property
    def is_participant(self) -> bool:
        return self.groups.filter(name=settings.GROUPS_PARTICIPANT).exists()

    def __str__(self):
        return str(self.get_username())
