from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from api.resources.account_resources import ChangePassword, ForgotPassword, \
    ResetPassword
from cdh.core.forms import TemplatedFormMixin, TemplatedForm


class CustomAuthenticationFrom(TemplatedFormMixin, AuthenticationForm):

    error_messages = {
        "invalid_login": _(
            "Please enter a correct email address and password. Note that both "
            "fields may be case-sensitive."
        ),
    }

    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
            }
        )
    )


#
# Password forms
#

class EnterTokenForm(TemplatedForm):
    token = forms.CharField(
        widget=forms.TextInput(attrs={
            'autofocus':   True,
            'placeholder': _('forms:forgot_password:token_placeholder')
        }),
    )


class ForgotPasswordForm(TemplatedForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autofocus':   True,
            'placeholder': _('forms:forgot_password:email_placeholder')
        }),
    )

    def __init__(self, *args, **kwargs):
        self.ldap = False
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        email = email.lower()

        req = ForgotPassword()
        req.email = email

        response = req.put()

        if not response.success and not response.ldap_blocked:
            raise forms.ValidationError(
                _('form:forgot_password:email_incorrect'),
                code='email_incorrect',
            )

        self.ldap = response.ldap_blocked

        return email


class ResetPasswordForm(TemplatedForm):
    error_messages = {
        'password_mismatch': _("forms:change_password:password_mismatch"),
        'token_incorrect':   _("forms:change_password:token_incorrect"),
    }

    token = forms.CharField(
        widget=forms.HiddenInput
    )

    new_password1 = forms.CharField(
        label=_('forms:change_password:new1'),
        strip=False,
        widget=forms.PasswordInput
    )

    new_password2 = forms.CharField(
        label=_('forms:change_password:new2'),
        strip=False,
        widget=forms.PasswordInput
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        token = self.cleaned_data.get('token')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch'
                )

        password_validation.validate_password(password2)

        req = ResetPassword()
        req.token = token
        req.new_password = password2

        response = req.put()

        if not response.success:
            raise forms.ValidationError(
                self.error_messages['token_incorrect'],
                code='token_incorrect',
            )

        return password2


class ChangePasswordForm(TemplatedForm):
    error_messages = {
        'password_mismatch':  _("forms:change_password:password_mismatch"),
        'password_incorrect': _("forms:change_password:password_incorrect"),
    }

    new_password1 = forms.CharField(
        label=_('forms:change_password:new1'),
        strip=False,
        widget=forms.PasswordInput
    )

    new_password2 = forms.CharField(
        label=_('forms:change_password:new2'),
        strip=False,
        widget=forms.PasswordInput
    )

    old_password = forms.CharField(
        label=_('forms:change_password:old'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autofocus': True
        }),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch'
                )

        password_validation.validate_password(password2)

        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password1')

        # If we already have errors on record from the new password fields,
        # we shouldn't do the request.
        if self.errors:
            return old_password

        req = ChangePassword()
        req.current_password = old_password
        req.new_password = new_password

        response = req.put()

        if not response.success:
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )

        return old_password
