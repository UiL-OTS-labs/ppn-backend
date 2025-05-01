from django.db import models


class LeaderPhoto(models.Model):

    leader = models.ForeignKey(
        'apiauth.RemoteApiUser',
        on_delete=models.CASCADE
    )

    photo = models.ImageField(
        blank=True
    )
