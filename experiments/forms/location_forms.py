from django import forms

from cdh.core.forms import TemplatedModelForm

from ..models import Location


class CreateLocationForm(TemplatedModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        widgets = {
            'name': forms.TextInput,
        }
