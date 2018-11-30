from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _

from .experiment_models import Experiment


class DefaultCriteria(models.Model):

    MULTILINGUAL = (
        ('Y', _('default_criteria:attribute:multilingual:yes')),
        ('N', _('default_criteria:attribute:multilingual:no')),
        ('I', _('experiments:globals:indifferent')),
    )

    SEX = (
        ('M', _('default_criteria:attribute:sex:male')),
        ('F', _('default_criteria:attribute:sex:female')),
        ('I', _('experiments:globals:indifferent')),
    )

    HANDEDNESS = (
        ('L', _('default_criteria:attribute:handedness:lefthanded')),
        ('R', _('default_criteria:attribute:handedness:righthanded')),
        ('I', _('experiments:globals:indifferent')),
    )

    DYSLEXIA = (
        ('Y', _('default_criteria:attribute:dyslexia:yes')),
        ('N', _('default_criteria:attribute:dyslexia:no')),
        ('I', _('experiments:globals:indifferent')),
    )

    SOCIAL_STATUS = (
        ('S', _('default_criteria:attribute:social_status:student')),
        ('O', _('default_criteria:attribute:social_status:other')),
        ('I', _('experiments:globals:indifferent')),
    )

    experiment = models.OneToOneField(
        Experiment,
        on_delete=models.CASCADE
    )

    language = models.TextField(
        _('default_criteria:attribute:language'),
        default='nl',
    )

    multilingual = models.CharField(
        _('default_criteria:attribute:multilingual'),
        choices=MULTILINGUAL,
        max_length=1,
        blank=False,
        default='I',
    )

    sex = models.CharField(
        _('default_criteria:attribute:sex'),
        choices=SEX,
        max_length=1,
        blank=False,
        default='I',
    )

    handedness = models.CharField(
        _('default_criteria:attribute:handedness'),
        choices=HANDEDNESS,
        max_length=1,
        blank=False,
        default='I',
    )

    dyslexia = models.CharField(
        _('default_criteria:attribute:dyslexia'),
        choices=DYSLEXIA,
        max_length=1,
        blank=False,
        default='I',
    )

    social_status = models.CharField(
        _('default_criteria:attribute:social_status'),
        choices=SOCIAL_STATUS,
        max_length=1,
        blank=False,
        default='I',
    )

    min_age = models.IntegerField(
        _('default_criteria:attribute:min_age'),
        validators=[MinValueValidator(-1)],
        default=-1,
        help_text=_('default_criteria:attribute:min_age:help_text'),
    )

    max_age = models.IntegerField(
        _('default_criteria:attribute:max_age'),
        validators=[MinValueValidator(-1)],
        default=-1,
        help_text=_('default_criteria:attribute:max_age:help_text'),
    )