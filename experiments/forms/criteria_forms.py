from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from cdh.core.forms import BootstrapRadioSelect
from main.forms import PPNTemplatedForm, PPNTemplatedModelForm

from ..models import Criterion, DefaultCriteria
from ..widgets import LanguageWidget


class DefaultCriteriaForm(PPNTemplatedModelForm):
    class Meta:
        model = DefaultCriteria
        fields = '__all__'
        widgets = {
            'experiment':    forms.HiddenInput,
            'language':      LanguageWidget,
            'multilingual':  BootstrapRadioSelect,
            'sex':           BootstrapRadioSelect,
            'handedness':    BootstrapRadioSelect,
            'dyslexia':      BootstrapRadioSelect,
            'social_status': BootstrapRadioSelect,
        }

    always_show_help_column = False

    def __init__(self, *args, **kwargs):
        # This removes the colon from the labels. Without it Django is very
        # inconsistent in it's use, so we just remove it
        kwargs.setdefault('label_suffix', '')
        super(DefaultCriteriaForm, self).__init__(*args, **kwargs)


class CriterionForm(PPNTemplatedModelForm):
    class Meta:
        model = Criterion
        fields = ['name_form', 'name_natural', 'values']
        widgets = {
            'name_form':     forms.TextInput,
            'name_natural':  forms.TextInput,
            'values':        forms.TextInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.criterionanswer_set.count() != 0:
            self.fields['values'].disabled = True

    def clean_name_form(self):
        """Slugifies the form name"""
        return slugify(self.cleaned_data['name_form'])

    def clean_values(self):
        """
        Removes any whitespace in the values
        """
        values = self.cleaned_data['values'].split(',')
        cleaned = []

        for value in values:
            cleaned.append(value.strip())

        return ','.join(cleaned)

    def clean_correct_value(self):
        """Makes sure correct_value is actually one of the values that can be
        chosen.
        """
        values = self.cleaned_data['values'].strip().split(',')
        correct_value = self.cleaned_data['correct_value']

        if correct_value not in values:
            raise forms.ValidationError(_(
                'criteria:form:correct_value:error:not_a_value'))

        return correct_value


class ExperimentCriterionForm(PPNTemplatedForm):

    name_form = forms.CharField(
        label=_('criterion:attribute:name_form'),
        help_text=_('criterion:attribute:name_form:help'),
    )

    name_natural = forms.CharField(
        label=_('criterion:attribute:name_natural'),
        help_text=_('criterion:attribute:name_natural:help'),
    )

    values = forms.CharField(
        label=_('criterion:attribute:values'),
        help_text=_('criterion:attribute:values:help'),
    )

    correct_value = forms.CharField(
        label=_('experiment_criterion:attribute:correct_value'),
        help_text=_('experiment_criterion:attribute:correct_value:help'),
    )

    message_failed = forms.CharField(
        label=_('experiment_criterion:attribute:message_failed'),
        help_text=_('experiment_criterion:attribute:message_failed:help'),
        widget=forms.Textarea({'cols': 35}),
    )

    def clean_name_form(self):
        """Slugifies the form name"""
        return slugify(self.cleaned_data['name_form'])

    def clean_values(self):
        """
        Removes any whitespace in the values
        """
        values = self.cleaned_data['values'].split(',')
        cleaned = []

        for value in values:
            cleaned.append(value.strip())

        return ','.join(cleaned)

    def clean_correct_value(self):
        """Makes sure correct_value is actually one of the values that can be
        chosen.
        """
        values = self.cleaned_data['values'].strip().split(',')
        correct_value = self.cleaned_data['correct_value']

        if correct_value not in values:
            raise forms.ValidationError(_(
                'criteria:form:correct_value:error:not_a_value'))

        return correct_value
