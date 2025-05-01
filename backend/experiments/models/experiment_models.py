from datetime import datetime, timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Count, F
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import get_current_timezone

from leaders.models import Leader
from .location_models import Location
from ..emails import InviteEmail, ReminderEmail, ConfirmationEmail


def _get_dt_2_hours_ago() -> datetime:
    return datetime.now(tz=get_current_timezone()) - timedelta(hours=2)


class Experiment(models.Model):

    name = models.TextField(
        _('experiment:attribute:name')
    )

    duration = models.TextField(
        _('experiment:attribute:duration')
    )

    compensation = models.TextField(
        _('experiment:attribute:compensation')
    )

    task_description = models.TextField(
        _('experiment:attribute:task_description')
    )

    additional_instructions = models.TextField(
        _('experiment:attribute:additional_instructions'),
        blank=True,
    )

    confirmation_email = models.TextField(
        _('experiment:attribute:confirmation_email'),
        help_text=ConfirmationEmail.help_text,
        default=ConfirmationEmail.default_content,
    )

    invite_email = models.TextField(
        _('experiment:attribute:invite_email'),
        help_text=InviteEmail.help_text,
        default=InviteEmail.default_content,
    )

    reminder_email = models.TextField(
        _('experiment:attribute:reminder_email'),
        help_text=ReminderEmail.help_text,
        default=ReminderEmail.default_content,
    )

    location = models.ForeignKey(
        Location,
        verbose_name=_('experiment:attribute:location'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    use_timeslots = models.BooleanField(
        _('experiment:attribute:use_timeslots'),
        default=True,
        help_text=_('experiment:attribute:use_timeslots:help_text'),
    )

    default_max_places = models.PositiveSmallIntegerField(
        _('experiment:attribute:default_max_places'),
        validators=[
            MinValueValidator(1),
        ],
        help_text=_('experiment:attribute:default_max_places:help_text'),
        default=1,
    )

    open = models.BooleanField(
        _('experiment:attribute:open'),
        default=False,
        help_text=_('experiment:attribute:open:help_text'),
    )

    public = models.BooleanField(
        _('experiment:attribute:public'),
        default=True,
        help_text=_('experiment:attribute:public:help_text'),
    )

    participants_visible = models.BooleanField(
        _('experiment:attribute:participants_visible'),
        default=True,
        help_text=_('experiment:attribute:participants_visible:help_text'),
    )

    excluded_experiments = models.ManyToManyField(
        "self",
        verbose_name=_('experiment:attribute:excluded_experiments'),
        blank=True,
        help_text=_('experiment:attribute:excluded_experiments:help_text'),
    )

    leader = models.ForeignKey(
        Leader,
        verbose_name=_("experiment:attribute:leader"),
        on_delete=models.SET_DEFAULT,
        related_name='experiments',
        default=1,
        help_text=_("experiment:attribute:leader:help_text"),
    )

    additional_leaders = models.ManyToManyField(
        Leader,
        verbose_name=_("experiment:attribute:additional_leaders"),
        related_name='secondary_experiments',
        blank=True,
        help_text=_("experiment:attribute:additional_leaders:help_text"),
    )

    @property
    def all_leaders_str(self):
        leaders = self.leader.name

        # 0 should be seen as false
        if num_additional_leaders := self.additional_leaders.count():
            last_leader = self.additional_leaders.last()
            others = self.additional_leaders.exclude(pk=last_leader.pk)

            # If there's one additional, don't add the comma as it looks weird
            if num_additional_leaders > 1:
                leaders += ", "

            leaders += ", ".join(
                [x.name for x in others]
            )
            leaders += f" en {last_leader.name}"

        return leaders

    def n_timeslot_places(self):
        """Returns the sum of all timeslot places this experiment has.
        Used for experiment index page. Used to be an aggregate method in
        that view, but it turns out it was not playing well with the other
        aggregates (it was taking those as a multiply number, due to weird
        join behaviour).

        This function is basically me giving up....
        """
        return sum([x.max_places for x in self.timeslot_set.all()])

    def has_free_places(self):
        """
        Returns if this experiment is available for new participants. If
        this experiment uses timeslots, it will return the same as
        has_free_timeslots. Otherwise, it will check if the number of existing
        appointments is lower than the number of maximum appointments.
        :return:
        """
        if self.use_timeslots:
            return self.has_free_timeslots()

        return self.appointments.count() < self.default_max_places

    def has_free_timeslots(self):
        """
        Returns if this experiment still has free timeslots available for
        registering. If this experiment does not use timeslots, it will always
        return False.
        :return:
        """
        return self.timeslot_set.annotate(
            num_appointments=Count('appointments')
        ).filter(
            datetime__gt=_get_dt_2_hours_ago(),
            max_places__gt=F('num_appointments')
        ).exists()

    def __str__(self):
        return self.name
