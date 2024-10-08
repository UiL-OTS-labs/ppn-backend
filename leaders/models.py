from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.auth.models import ApiUser


class Leader(models.Model):

    name = models.TextField()

    phonenumber = models.TextField()

    api_user = models.OneToOneField(
        ApiUser,
        # Not really going to happen, but we want to handle cascading through
        # signals
        null=True,
        on_delete=models.SET_NULL
    )

    @property
    def email(self):
        return self.api_user.email

    def is_active_leader(self) -> bool:
        if self.api_user.groups.filter(name=settings.LEADER_GROUP):
            return self.api_user.is_active

        return False

    def __str__(self):
        if not self.is_active_leader():
            return _("leader:inactive").format(self.name)

        return self.name
