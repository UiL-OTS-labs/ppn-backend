from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from cdh.core.forms import BootstrapCheckboxInput, \
    BootstrapRadioSelect, BootstrapSelect, TinyMCEWidget
from cdh.mail.widgets import EmailContentEditWidget
from main.forms import PPNTemplatedModelForm

from ..models import Experiment


class ExperimentForm(PPNTemplatedModelForm):
    class Meta:
        model = Experiment
        fields = [
            'name',
            'duration',
            'compensation',
            'task_description',
            'additional_instructions',
            'location',
            'use_timeslots',
            'default_max_places',
            'open',
            'public',
            'participants_visible',
            'excluded_experiments',
            'leader',
            'additional_leaders',
        ]
        widgets = {
            'name':         forms.TextInput,
            'duration':     forms.TextInput,
            'compensation': forms.TextInput,
            'use_timeslots': BootstrapRadioSelect(choices=(
                (True, _("experiment:form:use_timeslots:true")),
                (False, _("experiment:form:use_timeslots:false")),
            )),
            'task_description': TinyMCEWidget,
            'additional_instructions': TinyMCEWidget,
            'open': BootstrapCheckboxInput,
            'public': BootstrapCheckboxInput,
            'participants_visible': BootstrapCheckboxInput,
            'location': BootstrapSelect,
            'leader': BootstrapSelect,
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


class ExperimentEmailTemplatesForm(PPNTemplatedModelForm):
    class Meta:
        model = Experiment
        fields = [
            'invite_email',
            'reminder_email',
            'confirmation_email',
        ]
        widgets = {
            # we set the url in the init, as we need the experiment's pk
            'invite_email': EmailContentEditWidget(None),
            'reminder_email': EmailContentEditWidget(None),
            'confirmation_email': EmailContentEditWidget(None),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['invite_email'].widget.preview_url = reverse(
            'experiments:mail_preview',
            args=[self.instance.pk]
        )
        self.fields['reminder_email'].widget.preview_url = reverse(
            'experiments:reminder_preview',
            args=[self.instance.pk]
        )
        self.fields['confirmation_email'].widget.preview_url = reverse(
            'experiments:confirmation_preview',
            args=[self.instance.pk]
        )
