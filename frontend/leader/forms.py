from django import forms

from cdh.core.forms import TemplatedForm


class ChangeProfileForm(TemplatedForm):
    name = forms.Field()

    email = forms.EmailField(required=False)

    phone = forms.Field()

    photo = forms.ImageField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(ChangeProfileForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'disabled': 'disabled'
        })


class TimeSlotForm(TemplatedForm):
    datetime = forms.DateTimeField()

    max_places = forms.IntegerField()

    experiment = forms.Field(
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        super(TimeSlotForm, self).__init__(*args, **kwargs)

        self.fields['max_places'].widget.attrs.update(
            {
                'min': 1,
                'max': 10,
            }
        )


class AddCommentForm(TemplatedForm):
    show_valid_fields = False

    participant = forms.Field(
        widget=forms.TextInput(
            attrs={
                'disabled': 'disabled'
            },
        ),
        required=False
    )

    experiment = forms.Field(
        widget=forms.TextInput(
            attrs={
                'disabled': 'disabled'
            },
        ),
        required=False
    )

    comment = forms.Field(
        widget=forms.Textarea(),
        required=False
    )
