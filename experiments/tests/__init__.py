from api.auth.models import ApiUser
from leaders.models import Leader
from ..models import Location

def _get_or_create_leader() -> Leader:
    if Leader.objects.exists():
        return Leader.objects.first()
    user = ApiUser.objects.create()
    return Leader.objects.create(api_user=user)


def _get_or_create_location() -> Location:
    if Location.objects.exists():
        return Location.objects.first()
    return Location.objects.create(name="Cyberspace")
