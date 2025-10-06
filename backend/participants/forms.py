from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import gettext_lazy as _

from cdh.core.forms import (SearchableSelectWidget, TelephoneInput,
                            BootstrapRadioSelect,
                            BootstrapCheckboxInput, )
from main.forms import PPNTemplatedForm, PPNTemplatedModelForm

from .models import CriterionAnswer, Participant
from .widgets import ParticipantLanguageWidget, ParticipantSexWidget


class ParticipantForm(PPNTemplatedModelForm):
    class Meta:
        model = Participant
        fields = [
            'name', 'email', 'language', 'dyslexic', 'birth_date',
            'multilingual', 'phonenumber', 'handedness', 'sex',
            'social_status', 'email_subscription', 'capable'
        ]
        widgets = {
            'name': forms.TextInput,
            'language': ParticipantLanguageWidget,
            'phonenumber': TelephoneInput,
            'handedness': BootstrapRadioSelect,
            'sex': ParticipantSexWidget,
            'social_status': BootstrapRadioSelect,
            'dyslexic': BootstrapCheckboxInput,
            'email_subscription': BootstrapCheckboxInput,
            'capable': BootstrapCheckboxInput,
        }



    def __init__(self, *args, **kwargs):
        super(ParticipantForm, self).__init__(*args, **kwargs)

        self.fields['multilingual'].widget = BootstrapRadioSelect(choices=(
            (None, '---------'),
            (True, _("participants:multilingual:many")),
            (False, _("participants:multilingual:one")),
        ))
    
    def clean_email(self):
        email = self.cleaned_data.get('email')      
        filtered = Participant.objects.find_by_email(email)

        already_known = len(filtered) != 0
        if already_known:
            same_user = self.instance.id == filtered[0].id
            if not same_user:
                raise ValidationError(
                    _('Deze email is al in gebruik door een andere participant.'),
                    code='email_exists'
                )
        return email

class CriterionAnswerForm(forms.ModelForm):
    class Meta:
        model = CriterionAnswer
        fields = ['answer']
        widgets = {
            'answer': forms.RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super(CriterionAnswerForm, self).__init__(*args, **kwargs)

        self.fields['answer'].label = self.instance.criterion.name_natural
        self.fields['answer'].widget.choices = \
            self.instance.criterion.choices_tuple


class ParticipantMergeForm(PPNTemplatedForm):

    old_participant = forms.ModelChoiceField(
        Participant.objects.all(),
        label=_('participants:merge_form:field:old_participant'),
        empty_label=_('Type om participant op te zoeken'),
        widget=SearchableSelectWidget,
    )

    new_participant = forms.ModelChoiceField(
        Participant.objects.all(),
        label=_('participants:merge_form:field:new_participant'),
        empty_label=_('Type om participant op te zoeken'),
        widget=SearchableSelectWidget,
    )
    

    def clean_new_participant(self):
        """This checks if two unique participants have been chosen"""
        data = self.cleaned_data

        if data['old_participant'] == data['new_participant']:
            raise ValidationError(
                _('participants:merge_form:validation:are_equal')
            )

        return data['new_participant']
