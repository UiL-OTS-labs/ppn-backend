from django.utils.translation import gettext_lazy as _

from cdh.rest import client as rest


#
# Default criteria
#

class DefaultCriteria(rest.Resource):
    """
    This resources describes all default criteria for an experiment
    """
    id = rest.IntegerField()

    language = rest.TextField()

    multilingual = rest.TextField()

    sex = rest.TextField()

    handedness = rest.TextField()

    dyslexia = rest.TextField()

    social_status = rest.TextField()

    min_age = rest.IntegerField()

    max_age = rest.IntegerField()

    def get_language_display(self):
        if self.language == 'I':
            return _('globals:indifferent')

        return self.language

    def get_multilingual_display(self):
        if self.multilingual == 'I':
            return _('globals:indifferent')

        return self.multilingual

    def get_sex_display(self):
        if self.sex == 'I':
            return _('globals:indifferent')

        return self.sex

    def get_handedness_display(self):
        if self.handedness == 'I':
            return _('globals:indifferent')

        return self.handedness

    def get_social_status_display(self):
        if self.social_status == 'I':
            return _('globals:indifferent')

        return self.social_status

    def get_min_age_display(self):
        if self.min_age == -1:
            return _('globals:indifferent')

        return self.min_age

    def get_max_age_display(self):
        if self.max_age == -1:
            return _('globals:indifferent')

        return self.max_age


#
# A set of resources for specific criteria
#


class Criterion(rest.Resource):
    """
    This resources represents a specific criterion
    """
    id = rest.IntegerField()

    name_form = rest.TextField()

    name_natural = rest.TextField()

    values = rest.TextField()

    @property
    def value_list(self):
        return self.values.split(',')


class ExperimentCriterion(rest.Resource):
    """
    This resources represents the link between an experiment and a criterion.

    It also lists the correct value and error message for this experiment.
    """
    id = rest.IntegerField()

    criterion = rest.ResourceField(Criterion)

    correct_value = rest.TextField()

    message_failed = rest.TextField()


class ExperimentCriteria(rest.ResourceCollection):
    """
    A collection of specific criteria for an experiment.
    """

    class Meta:
        resource = ExperimentCriterion
