from django import forms
from django.utils.translation import gettext_lazy as _
from cdh.core.forms import TemplatedModelForm, BootstrapCheckboxInput, \
    BootstrapRadioSelect, BootstrapSelect

from ..models import Experiment


class ExperimentForm(TemplatedModelForm):
    class Meta:
        model = Experiment
        fields = '__all__'
        widgets = {
            'name':         forms.TextInput,
            'duration':     forms.TextInput,
            'compensation': forms.TextInput,
            'use_timeslots': BootstrapRadioSelect(choices=(
                (True, _("experiment:form:use_timeslots:true")),
                (False, _("experiment:form:use_timeslots:false")),
            )),
            'task_description': forms.Textarea({
                'rows': 7,
            }),
            'additional_instructions': forms.Textarea({
                'rows': 7
            }),
            'open': BootstrapCheckboxInput,
            'public': BootstrapCheckboxInput,
            'participants_visible': BootstrapCheckboxInput,
            'location': BootstrapSelect,
            'leader': BootstrapSelect,
            # TODO: excluded experiment and additional leaders select
        }

    def __init__(self, *args, **kwargs):
        super(ExperimentForm, self).__init__(*args, **kwargs)

        self.fields['default_max_places'].widget.attrs.update(
            {
                'min': 1,
            }
        )

        # If we are updating an experiment, make sure you cannot exclude the
        # experiment you are updating!
        if self.instance:
            other_experiments = Experiment.objects.exclude(pk=self.instance.pk)
            self.fields['excluded_experiments'].choices = [
                (x.pk, x.name) for x in other_experiments
            ]
