from django.db import IntegrityError
from django.utils.functional import cached_property

from cdh.rest import client as rest
from leader.models import LeaderPhoto


#
# Leader resources
#

class Leader(rest.Resource):
    """
    Describes a leader, can be used to retrieve the current leader's profile
    or in other resources. A put operation will update the name and
    phonenumber (the rest is ignored). NOTE: put is only supported for
    editting a leader's own profile. Putting with a different account WILL
    result in an error.
    """

    class Meta:
        path = '/api/leader/'
        supported_operations = [rest.Operations.put, rest.Operations.get]
        default_return_resource = 'api.Leader'

    id = rest.IntegerField()

    name = rest.TextField()

    phonenumber = rest.TextField(blank=True, null=True)

    email = rest.TextField()

    api_user = rest.ResourceField('apiauth.ApiUserResource')

    def photo(self):
        leader_id = self.api_user
        if not isinstance(leader_id, int):
            leader_id = leader_id.id

        try:
            obj, created = LeaderPhoto.objects.get_or_create(
                leader_id=leader_id)

            return obj.photo

        except IntegrityError:
            return None


class Leaders(rest.ResourceCollection):
    """
    A collection of leaders, used for the experiment's 'additional_leaders'
    field.
    """

    class Meta:
        resource = Leader
