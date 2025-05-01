from cdh.rest import client as rest
from api.resources.generic_resources import SuccessResponse


class Comment(rest.Resource):
    """
    This resources can be used to add a comment for a participant (for an
    experiment).
    """
    class Meta:
        path = '/api/leader/add_comment/'
        supported_operations = [rest.Operations.put]
        default_return_resource = SuccessResponse
        default_send_as_json = True

    experiment = rest.IntegerField()

    participant = rest.IntegerField()

    comment = rest.TextField()
