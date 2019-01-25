from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.auth.authenticators import JwtAuthentication
from api.permissions import IsPermittedClient


class ChangePasswordView(views.APIView):
    permission_classes = (IsPermittedClient, IsAuthenticated)
    authentication_classes = (JwtAuthentication, )

    def post(self, request):

        user = request.user

        post_data = self.request.POST

        success = False

        if user.check_password(post_data['current_password']):

            user.set_password(post_data['new_password'])
            user.passwords_needs_change = False
            user.save()

            success = True

        return Response({
            'success': success
        })
