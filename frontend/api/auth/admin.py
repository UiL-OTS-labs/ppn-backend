from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from api.auth.models import RemoteApiUser


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    is_active = forms.BooleanField(disabled=True)
    is_superuser = forms.BooleanField(disabled=True)
    is_staff = forms.BooleanField(disabled=True)
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = RemoteApiUser
        fields = ('id', 'password', 'is_active', 'is_superuser', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = None

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'is_superuser', 'is_staff')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('id', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('id',)
    ordering = ('id',)
    filter_horizontal = ()

    def has_add_permission(self, request):
        return False


# Now register the new UserAdmin...
admin.site.register(RemoteApiUser, UserAdmin)
