import braces.views as braces
from django.urls import reverse_lazy as reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from django.views import generic

from participants.models import Participant
from cdh.core.views import RedirectActionView
from cdh.core.views.mixins import RedirectSuccessMessageMixin


from datamanagement.forms import ThresholdsEditForm
from datamanagement.utils.comments import delete_comments, get_comment_counts
from datamanagement.utils.common import get_thresholds_model
from datamanagement.utils.exp_part_visibility import \
    get_experiments_with_visibility, hide_part_from_exp
from datamanagement.utils.invitations import delete_invites, get_invite_counts
from datamanagement.utils.participants import \
    delete_participant, get_participants_with_appointments, \
    get_participants_without_appointments
from experiments.models import Experiment


# TODO: write tests


class OverviewView(braces.LoginRequiredMixin, generic.TemplateView):
    template_name = 'datamanagement/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['invites'] = get_invite_counts()
        context['comments'] = get_comment_counts()
        context['participants'] = get_participants_with_appointments()
        context['participants_no_app'] = get_participants_without_appointments()
        context['participants_num'] = len(context['participants']) + \
                                      len(context['participants_no_app'])
        context['exp_part_visible'] = get_experiments_with_visibility()

        return context


class ThresholdsEditView(braces.LoginRequiredMixin, generic.UpdateView):
    form_class = ThresholdsEditForm
    template_name = 'datamanagement/edit_thresholds.html'
    success_url = reverse('datamanagement:overview')

    def get_object(self, queryset=None):
        return get_thresholds_model()


class DeleteParticipantView(braces.LoginRequiredMixin,
                            RedirectSuccessMessageMixin,
                            RedirectActionView):

    def action(self, request):

        if delete_participant(self.participant, self.request.user):
            self.success_message = _(
                'datamanagement:messages:deleted_participant'
            )
        else:
            self.success_message = _('datamanagement:messages:refused_deletion')


    @cached_property
    def participant(self):
        pk = self.kwargs.get('participant')

        return Participant.objects.get(pk=pk)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('datamanagement:overview') + \
               "#collapse-participants"


class HideParticipantsView(braces.LoginRequiredMixin,
                           RedirectSuccessMessageMixin,
                           RedirectActionView):

    def action(self, request):
        hide_part_from_exp(self.experiment)

    @cached_property
    def experiment(self):
        pk = self.kwargs.get('experiment')

        return Experiment.objects.get(pk=pk)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('datamanagement:overview') + \
               "#collapse-exp_part_visibility"

    def get_success_message(self):
        return _('datamanagement:messages:hid_participants').format(
            self.experiment
        )


class DeleteInvitesView(braces.LoginRequiredMixin,
                        RedirectSuccessMessageMixin,
                        RedirectActionView):

    def action(self, request):
        delete_invites(self.experiment, self.request.user)

    @cached_property
    def experiment(self):
        pk = self.kwargs.get('experiment')

        return Experiment.objects.get(pk=pk)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('datamanagement:overview') + "#collapse-invites"

    def get_success_message(self):
        return _('datamanagement:messages:deleted_invites').format(
            self.experiment
        )


class DeleteCommentsView(braces.LoginRequiredMixin,
                         RedirectSuccessMessageMixin,
                         RedirectActionView):
    def action(self, request):
        delete_comments(self.experiment, self.request.user)

    @cached_property
    def experiment(self):
        pk = self.kwargs.get('experiment')

        return Experiment.objects.get(pk=pk)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('datamanagement:overview') + "#collapse-comments"

    def get_success_message(self):
        return _('datamanagement:messages:deleted_comments').format(
            self.experiment
        )
