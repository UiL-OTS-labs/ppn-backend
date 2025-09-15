from braces import views as braces
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages import error
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.views import generic

from api.resources.participant_resources import Appointments, \
    RequiredRegistrationFields
from main.mixins import ExperimentObjectMixin, OverrideLanguageMixin
from participant.forms import BaseRegisterForm
from participant.utils import experiment_is_open, get_register_form, \
    submit_register_form


class ExperimentRegisterMixin(ExperimentObjectMixin):
    template_name = 'participant/register.html'

    def __init__(self):
        super(ExperimentRegisterMixin, self).__init__()
        self.success = None
        self.recoverable = None
        self.messages = []

    def get_context_data(self, **kwargs):
        context = super(ExperimentRegisterMixin, self).get_context_data(
            **kwargs
        )

        context['success'] = self.success
        context['recoverable'] = self.recoverable
        context['api_messages'] = self.messages
        context['experiment'] = self.experiment

        return context

    @cached_property
    def _required_fields(self):
        return '__all__'

    def form_valid(self, form):
        success, recoverable, messages = submit_register_form(
            form,
            self.experiment,
            self._required_fields,
            self.request,
        )

        if not success and messages:
            error(self.request,
                  'Waarschuwing! Je bent (nog) niet aangemeld! Zie onderaan de '
                  'pagina voor details.',
                  )

        self.success = success
        self.recoverable = recoverable
        self.messages = messages

        if success:
            return HttpResponseRedirect(
                reverse(
                    'participant:register_success',
                    args=[self.experiment.id]
                )
            )

        return self.get(self.request, [], {})

    def get_form(self, form_class=None):
        base_form = super(ExperimentRegisterMixin, self).get_form(form_class)

        return get_register_form(
            base_form,
            self.experiment,
            self._required_fields
        )


class RegisterView(OverrideLanguageMixin,
                   ExperimentRegisterMixin,
                   generic.FormView):
    form_class = BaseRegisterForm
    language_override = 'nl'

    def dispatch(self, request, *args, **kwargs):
        try:
            # You might ask, why not just do the return in the body of this
            # if-statement. Well, that's because the very act of calling
            # self.experiment might raise ObjectDoesNotExist as well!
            # This way, we can do both in one except.
            if not experiment_is_open(self.experiment):
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            return HttpResponseRedirect(
                reverse('participant:closed_experiment')
            )

        # If there's a participant logged in, redirect to the right version
        # Except for when a leader wants to view their experiment page
        # (To avoid confused mails about not seeing a correct form).
        if request.user.is_authenticated and request.user.is_participant and \
                not self.experiment.is_leader(request.user):
            args = [self.kwargs.get('experiment')]
            return HttpResponseRedirect(
                reverse('participant:register_logged_in', args=args)
            )

        return super(RegisterView, self).dispatch(request, *args, **kwargs)


class AuthenticatedRegisterView(braces.LoginRequiredMixin,
                                OverrideLanguageMixin,
                                ExperimentRegisterMixin,
                                generic.FormView):
    form_class = BaseRegisterForm
    language_override = 'nl'

    def get_context_data(self, **kwargs):
        context = super(AuthenticatedRegisterView, self).get_context_data(
            **kwargs
        )

        # Don't add anything if we are submitting the form!
        if getattr(self, 'success') is not None:
            return context

        appointments = Appointments.client.get()

        # Check if this participant already has an appointment for this
        # experiment and add relevant context if so
        for appointment in appointments:
            if self.experiment.id == appointment.experiment.id:
                context['already_registered'] = True

                if 'messages' in context:
                    context['messages'].append(
                        self._already_registered_message
                    )
                else:
                    context['messages'] = [
                        self._already_registered_message
                    ]

                break

        return context

    @property
    def _already_registered_message(self):
        return mark_safe(
            "Je bent al ingeschreven voor dit experiment. Klik <a href=\"{}\">"
            "hier</a> om je uit te schrijven.".format(
                reverse('participant:appointments')
            ))

    def dispatch(self, request, *args, **kwargs):
        try:
            # You might ask, why not just do the return in the body of this
            # if-statement. Well, that's because the very act of calling
            # self.experiment might raise ObjectDoesNotExist as well!
            # This way, we can do both in one except.
            if not experiment_is_open(self.experiment):
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            return HttpResponseRedirect(
                reverse('participant:closed_experiment')
            )

        user = request.user
        # If there isn't a participant logged in, redirect to the right version
        # The hasattr is there because AnonymousUser doesn't have is_participant
        if not hasattr(user, 'is_participant') or not user.is_participant:
            args = [self.kwargs.get('experiment')]
            return HttpResponseRedirect(
                reverse('participant:register', args=args)
            )

        return super(AuthenticatedRegisterView, self).dispatch(
            request,
            *args,
            **kwargs
        )

    @cached_property
    def _required_fields(self):
        fields = RequiredRegistrationFields.client.get(
            experiment=self.experiment.id
        ).fields

        return list(fields)


class RegisterSuccessView(OverrideLanguageMixin, ExperimentObjectMixin,
                          generic.TemplateView):
    template_name = 'participant/register_success.html'
    language_override = 'nl'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )
        context['experiment'] = self.experiment

        return context


class ClosedExperimentView(OverrideLanguageMixin, generic.TemplateView):
    template_name = 'participant/closed_experiment.html'
    language_override = 'nl'
