from cdh.core.forms import TemplatedModelForm

from datamanagement.models import Thresholds
from datamanagement.widgets import TimespanWidget


class ThresholdsEditForm(TemplatedModelForm):
    class Meta:
        model = Thresholds
        fields = '__all__'
        widgets = {
            'participants_with_appointment':    TimespanWidget(),
            'participants_without_appointment': TimespanWidget(),
            'participant_visibility': TimespanWidget(
                default_display_mode='months'
            ),
            'comments':                         TimespanWidget(),
            'invites':                          TimespanWidget(
                default_display_mode='months'
            ),
        }
