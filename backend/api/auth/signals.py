from django.db.models.signals import pre_delete
from django.dispatch import receiver

from api.auth.models import ApiUser
from leaders.models import Leader


@receiver(pre_delete, sender=ApiUser)
def on_api_user_delete(sender, instance, using, **kwargs):
    # Delete the leader as well
    if instance and instance.is_leader:
        try:
            # Try to retrieve the leader from DB. It might already be deleted!
            # (Happens when deleting a leader, which triggers the ApiUser
            # delete from a signal, but that instance isn't updated yet)
            leader = Leader.objects.get(pk=instance.leader.pk)
            leader.delete()
        except Leader.DoesNotExist:
            pass
