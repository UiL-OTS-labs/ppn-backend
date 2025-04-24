from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic

from api.resources import Admin
from api.resources.participant_resources import ValidateMailinglistToken, \
    UnsubscribeFromMailinglist
from cdh.rest.exceptions import ApiError
from main.mixins import OverrideLanguageMixin


class UnsubscribeFromMailinglistView(OverrideLanguageMixin,
                                     generic.TemplateView):
    template_name = 'participant/unsubscribe_mailinglist.html'
    language_override = 'nl'

    def get_context_data(self, **kwargs):
        context = super(UnsubscribeFromMailinglistView, self).get_context_data(
            **kwargs
        )

        context['token_valid'] = False
        context['email'] = None
        context['admin'] = Admin.client.get()

        try:
            validate = ValidateMailinglistToken()
            validate.token = self.kwargs.get('token', None)

            response = validate.put()

            context['token_valid'] = response.success
            context['email'] = response.email
        except ApiError:
            pass

        return context

    def post(self, request, token):
        unsub = UnsubscribeFromMailinglist()
        unsub.token = token
        unsub.put()

        messages.success(
            request,
            _('unsubscribe_mailinglist:messages:unsubscribed')
        )

        return HttpResponseRedirect(reverse('main:home'))
