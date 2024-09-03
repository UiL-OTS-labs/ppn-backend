import braces.views as braces
from cdh.mail.views import BaseEmailPreviewView
from django.contrib.messages import error, success
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from django.views import generic

from experiments.utils.invite import get_initial_invite_context, mail_invite
from main.utils import get_supreme_admin
from .mixins import ExperimentObjectMixin
from ..emails import InviteEmail
from ..utils.exclusion import get_eligible_participants_for_experiment


class InviteParticipantsForExperimentView(braces.LoginRequiredMixin,
                                          ExperimentObjectMixin,
                                          generic.TemplateView):
    template_name = 'experiments/invite.html'

    experiment_prefetch_related = ['experimentcriterion_set',
                                   'experimentcriterion_set__criterion',
                                   'additional_leaders']
    experiment_select_related = ['defaultcriteria', 'leader', ]

    def get_context_data(self, **kwargs):
        context = super(InviteParticipantsForExperimentView,
                        self).get_context_data(**kwargs)

        context['object_list'] = self.get_object_list()
        context['experiment'] = self.experiment
        context['admin'] = get_supreme_admin().get_full_name()
        context['invite_text'] = self.experiment.invite_email
        context['invite_mail_help'] = InviteEmail.help_text

        return context

    def get_object_list(self):
        participants = get_eligible_participants_for_experiment(
            self.experiment
        )

        for participant in participants:
            try:
                invite = participant.invitation_set.filter(
                    experiment=self.experiment
                ).order_by('-creation_date').first()
                participant.invite = invite
            except ObjectDoesNotExist:
                participant.invite = None

        return participants

    def post(self, request, *args, **kwargs):
        data = request.POST
        failed = False

        try:
            mail_invite(
                data.getlist('participants[]'),
                data.get('content'),
                self.experiment
            )
        except Exception as e:
            print(e)
            failed = True

        if failed:
            error(request, _('experiments:message:invite_failure'))
        else:
            success(request, _('experiments:message:invite_success'))

        return self.get(request)


class InviteEmailPreview(braces.LoginRequiredMixin, ExperimentObjectMixin,
                         BaseEmailPreviewView):
    email_class = InviteEmail

    def post(self, request, experiment):
        return super(InviteEmailPreview, self).post(request)

    def get_preview_context(self):
        return get_initial_invite_context(self.experiment)

