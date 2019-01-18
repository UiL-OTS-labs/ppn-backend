from rest_framework import serializers

from experiments.models import Experiment


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        depth = 1
        fields = [
            'id', 'name', 'duration', 'compensation', 'task_description',
            'additional_instructions', 'open', 'public', 'participants_visible',
            'location', 'leader', 'additional_leaders', 'excluded_experiments',
            'timeslot_set', 'defaultcriteria', 'specific_criteria'
        ]

    specific_criteria = serializers.SerializerMethodField(
        source='experimentcriterium_set'
    )

    def get_specific_criteria(self, o):
        # Local import to prevent import cycles
        from .criteria_serializers import ExperimentCriteriumSerializer

        return ExperimentCriteriumSerializer(
            o.experimentcriterium_set.all(),
            many=True
        ).data