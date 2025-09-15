from cdh.rest import client as rest


class ApiGroupResource(rest.Resource):

    pk = rest.IntegerField()

    name = rest.TextField()


class ApiGroupResourceCollection(rest.ResourceCollection):

    class Meta:
        resource = ApiGroupResource


class ApiUserResource(rest.Resource):

    class Meta:
        path = '/api/auth/'
        supported_operations = [rest.Operations.get_over_post]

    id = rest.IntegerField()

    token = rest.TextField()

    is_active = rest.BoolField(default=False)

    is_admin = rest.BoolField(default=False)

    is_ldap_account = rest.BoolField(default=False)

    needs_password_change = rest.BoolField(default=False)

    groups = rest.CollectionField(ApiGroupResourceCollection)
