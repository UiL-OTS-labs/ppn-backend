from django.db.models.signals import pre_delete
from django.dispatch import receiver

from api.auth.models import ApiUser


@receiver(pre_delete, sender=ApiUser)
def on_api_user_delete(sender, instance, using, **kwargs):
    # Delete the leader as well
    if instance and instance.is_leader and instance.leader.id is not None:
        instance.leader.delete()
