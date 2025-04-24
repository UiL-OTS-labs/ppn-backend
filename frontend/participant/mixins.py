from braces.views import GroupRequiredMixin
from django.conf import settings
from django.contrib.auth.mixins import AccessMixin


class ParticipantRequiredMixin(GroupRequiredMixin):
    """This mixin requires that a user is also a participant. Shorthand mixin"""
    group_required = [settings.GROUPS_PARTICIPANT]
    raise_exception = True


class ParticipantForbiddenMixin(AccessMixin):
    """This mixin will allow anonymous users and users that are NOT in the
    participant group to view this view.

    It's basically a ¬ for the ParticipantRequiredMixin
    """
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        user = request.user

        if not user.is_anonymous:
            if user.groups.filter(name=settings.GROUPS_PARTICIPANT).exists():
                return self.handle_no_permission()

        return super(ParticipantForbiddenMixin, self).dispatch(
            request,
            *args,
            **kwargs
        )
