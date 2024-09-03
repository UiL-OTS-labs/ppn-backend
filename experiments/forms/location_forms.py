from django import forms

from main.forms import PPNTemplatedModelForm

from ..models import Location


class CreateLocationForm(PPNTemplatedModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            'name': forms.TextInput,
        }
