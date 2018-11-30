from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
import braces.views as braces

from main.views import RedirectSuccessMessageMixin
from ..models import Experiment
from ..forms import ExperimentForm


class ExperimentHomeView(braces.LoginRequiredMixin, generic.ListView):
    template_name = 'experiments/index.html'
    model = Experiment


class ExperimentCreateView(braces.LoginRequiredMixin, SuccessMessageMixin,
                           generic.CreateView):
    template_name = 'experiments/new.html'
    form_class = ExperimentForm
    success_message = _('experiments:message:create:success')

    def get_success_url(self):
        return reverse('experiments:default_criteria', args=[self.object.pk])


class ExperimentUpdateView(braces.LoginRequiredMixin, SuccessMessageMixin,
                           generic.UpdateView):
    template_name = 'experiments/edit.html'
    form_class = ExperimentForm
    model = Experiment
    success_message = _('experiments:message:update:success')
    success_url = reverse('experiments:home')


class ExperimentEditExcludedExperimentsView(braces.LoginRequiredMixin,
                                            generic.ListView):
    template_name = 'experiments/excluded_experiments.html'
    model = Experiment

    def get_queryset(self):
        return Experiment.objects.exclude(pk=self.kwargs['experiment'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExperimentEditExcludedExperimentsView, self)\
            .get_context_data(object_list=object_list, **kwargs)

        context['current_experiment'] = Experiment.objects.get(
            pk=self.kwargs['experiment']
        )

        return context


class ExperimentExcludeOtherExperimentView(braces.LoginRequiredMixin,
                                           RedirectSuccessMessageMixin,
                                           generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        experiment_pk = self.kwargs.get('current_experiment')
        exclude_experiment_pk = self.kwargs.get('exclude_experiment')

        current_experiment = Experiment.objects.get(pk=experiment_pk)
        exclude_experiment = Experiment.objects.get(pk=exclude_experiment_pk)

        if exclude_experiment in current_experiment.excluded_experiments.all():
            current_experiment.excluded_experiments.remove(exclude_experiment)
            self.success_message = _('experiments:message:exclude:included')
        else:
            current_experiment.excluded_experiments.add(exclude_experiment)
            self.success_message = _('experiments:message:exclude:excluded')

        current_experiment.save()

        return reverse('experiments:excluded_experiments', args=[experiment_pk])


class ExperimentSwitchOpenView(braces.LoginRequiredMixin,
                               RedirectSuccessMessageMixin,
                               generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')

        experiment = Experiment.objects.get(pk=pk)

        if experiment.open:
            experiment.open = False
            self.success_message = _('experiments:message:switch_open:closed')
        else:
            experiment.open = True
            self.success_message = _('experiments:message:switch_open:opened')

        experiment.save()

        return reverse('experiments:home')


class ExperimentSwitchPublicView(braces.LoginRequiredMixin,
                                 RedirectSuccessMessageMixin,
                                 generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')

        experiment = Experiment.objects.get(pk=pk)

        if experiment.public:
            experiment.public = False
            self.success_message = _('experiments:message:switch_public:closed')
        else:
            experiment.public = True
            self.success_message = _('experiments:message:switch_public:opened')

        experiment.save()

        return reverse('experiments:home')


class ExperimentSwitchVisibleView(braces.LoginRequiredMixin,
                                  RedirectSuccessMessageMixin,
                                  generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')

        experiment = Experiment.objects.get(pk=pk)

        if experiment.participants_visible:
            experiment.participants_visible = False
            self.success_message = _(
                'experiments:message:switch_visible:visible'
            )
        else:
            experiment.participants_visible = True
            self.success_message = _(
                'experiments:message:switch_visible:invisible'
            )

        experiment.save()

        return reverse('experiments:home')
