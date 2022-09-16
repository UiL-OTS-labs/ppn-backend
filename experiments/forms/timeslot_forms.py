from django import forms

from cdh.core.forms import TemplatedModelForm

from ..models import TimeSlot


class TimeSlotForm(TemplatedModelForm):

    class Meta:
        model = TimeSlot
        fields = ['datetime', 'max_places', 'experiment']
        widgets = {
            'experiment': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super(TimeSlotForm, self).__init__(*args, **kwargs)

        self.fields['max_places'].widget.attrs.update(
            {
                'min': 1,
                'max': 10,
            }
        )


