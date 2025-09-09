import braces.views as braces
from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy as reverse
from django.utils.functional import cached_property
from django.utils.text import gettext_lazy as _
from django.views import generic
from cdh.core.views import FormSetUpdateView, RedirectActionView
from cdh.core.views.mixins import DeleteSuccessMessageMixin
from main.views import RedirectSuccessMessageMixin

from .forms import CriterionAnswerForm, ParticipantForm, ParticipantMergeForm
from .models import CriterionAnswer, Participant, SecondaryEmail
from .utils import merge_participants

from auditlog.enums import Event, UserType
import auditlog.utils.log as auditlog
from .utils.switch_main_email import switch_main_email


class ParticipantsHomeView(braces.LoginRequiredMixin, generic.ListView):
    template_name = 'participants/index.html'
    model = Participant

    def get_queryset(self):
        return self.model.objects.prefetch_related('secondaryemail_set')


class ParticipantDetailView(braces.LoginRequiredMixin,
                            generic.DetailView):
    model = Participant
    template_name = 'participants/detail.html'

    def get(self, request, *args, **kwargs):
        message = "Admin viewed participant '{}'".format(self.get_object())
        auditlog.log(
            Event.VIEW_SENSITIVE_DATA,
            message,
            self.request.user,
            UserType.ADMIN
        )

        return super().get(request, *args, **kwargs)


class ParticipantSwitchEmailView(braces.LoginRequiredMixin,
                                 RedirectSuccessMessageMixin,
                                 RedirectActionView):

    success_message = _('participants:messages:switched_emails')

    def action(self, request):
        participant_pk = self.kwargs.get('participant')
        se_pk = self.kwargs.get('pk')

        participant = Participant.objects.get(pk=participant_pk)
        se = SecondaryEmail.objects.get(pk=se_pk)

        switch_main_email(participant, se)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('participants:detail', args=[
            self.kwargs.get('participant')
        ])


class ParticipantUpdateView(braces.LoginRequiredMixin,
                            SuccessMessageMixin,
                            generic.UpdateView):
    model = Participant
    template_name = 'participants/edit.html'
    success_message = _('participants:messages:updated_participant')
    form_class = ParticipantForm
    secondary_email_formset = forms.inlineformset_factory(
        Participant,
        SecondaryEmail,
        fields=('email',),
        can_delete=True,
        extra=4
    )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['secondary_email_formset'] = kwargs.get(
            'secondary_email_formset',
            self.secondary_email_formset(instance=self.get_object())
        )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        formset = self.secondary_email_formset(request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        elif not form.is_valid():
            return self.form_invalid(form)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                secondary_email_formset=formset
            )
        )

    def form_valid(self, form, formset):
        message = "Admin updated participant '{}'".format(self.object)
        auditlog.log(
            Event.MODIFY_DATA,
            message,
            self.request.user,
            UserType.ADMIN
        )
        formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('participants:detail', args=[self.object.pk])


class ParticipantDeleteView(braces.LoginRequiredMixin,
                            DeleteSuccessMessageMixin, generic.DeleteView):
    success_url = reverse('participants:home')
    success_message = _('participants:messages:deleted_participant')
    template_name = 'participants/delete.html'
    model = Participant



class ParticipantSpecificCriteriaUpdateView(braces.LoginRequiredMixin,
                                            FormSetUpdateView):
    form = CriterionAnswerForm
    template_name = 'participants/specific_criteria.html'
    succes_url = reverse('participants:home')

    def get_queryset(self):
        return CriterionAnswer.objects.filter(participant=self.participant)

    def get_context_data(self, **kwargs):
        context = super(ParticipantSpecificCriteriaUpdateView,
                        self).get_context_data(**kwargs)

        context['participant'] = self.participant

        return context

    @cached_property
    def participant(self):
        participant_pk = self.kwargs.get('pk')

        return Participant.objects.get(pk=participant_pk)


class ParticipantMergeView(braces.LoginRequiredMixin, SuccessMessageMixin,
                           generic.FormView):
    success_url = reverse('participants:home')
    success_message = _('participants:messages:merged_participants')
    template_name = 'participants/merge.html'
    form_class = ParticipantMergeForm

    def form_valid(self, form):
        data = form.cleaned_data

        merge_participants(data['old_participant'], data['new_participant'])

        return super(ParticipantMergeView, self).form_valid(form)
