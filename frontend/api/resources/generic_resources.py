from cdh.rest import client as rest


class SuccessResponse(rest.Resource):
    """
    Generic response resources.

    It's used for most resources that command the backend to do something.
    """

    success = rest.BoolField()
