import re

from django.http import HttpResponseRedirect
from django.urls import reverse


class PasswordChangeMiddleware:
    """This middleware will force a user to change their password if
    specified to do so.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and \
                not re.match(r'^/change_password/?', request.path) and not \
                re.match(r'^/logout/?', request.path):

            if request.session.get('force_password_change', False):
                url = reverse('main:change_password')
                return HttpResponseRedirect(url)

        return self.get_response(request)
