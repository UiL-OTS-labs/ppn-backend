from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views import generic

from cdh.rest.exceptions import ApiError
from api.resources import Appointments
from api.resources.participant_resources import SendCancelToken, Appointment
from main.mixins import OverrideLanguageMixin


class CancelLandingView(OverrideLanguageMixin, generic.TemplateView):
    template_name = 'participant/appointments/cancel_landing.html'
    language_override = 'nl'

    def get(self, request, *args, **kwargs):
        # Redirect to 'My appointments' if a participant is logged in.
        if request.user.is_authenticated and request.user.is_participant:
            return HttpResponseRedirect(reverse('participant:appointments'))

        return super(CancelLandingView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'email' in request.POST:
            req = SendCancelToken()
            req.email = request.POST.get('email')
            req.put()

            messages.success(request, _('cancel_landing:message:send_token'))

        return self.get(request, *args, **kwargs)


class MyAppointmentsView(OverrideLanguageMixin,
                         generic.TemplateView):
    template_name = 'participant/appointments/appointments.html'
    language_override = 'nl'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not user.is_participant:
            if 'token' not in self.kwargs:
                return HttpResponseRedirect(reverse('main:login'))

        if not user.is_authenticated and 'token' not in self.kwargs:
            return HttpResponseRedirect(reverse('participant:cancel_landing'))

        return super(MyAppointmentsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MyAppointmentsView, self).get_context_data(**kwargs)

        try:
            kwargs = {}
            if 'token' in self.kwargs:
                kwargs['user_token'] = self.kwargs.get('token')

            context['appointments'] = Appointments.client.get(**kwargs)
            context['token'] = self.kwargs.get('token', None)
        except ApiError:
            pass

        return context


class CancelAppointmentView(OverrideLanguageMixin, generic.RedirectView):
    # Used to enforce dutch messages
    language_override = 'nl'

    def get_redirect_url(self, *args, **kwargs):
        args = []
        if 'token' in self.kwargs:
            args.append(self.kwargs.get('token'))

        return reverse('participant:appointments', args=args)

    def get(self, request, *args, **kwargs):
        kwargs = {
            'id': self.kwargs.get('appointment')
        }

        if 'token' in self.kwargs:
            kwargs['user_token'] = self.kwargs.get('token')

        Appointment.client.delete(**kwargs)

        messages.success(
            request,
            mark_safe(_('cancel:message:cancelled'))
        )

        return super(CancelAppointmentView, self).get(request, *args, **kwargs)
