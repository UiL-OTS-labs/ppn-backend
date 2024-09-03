from django.urls import path

from experiments.views import (ExperimentAppointmentsView,
                               InviteEmailPreview,
                               InviteParticipantsForExperimentView,
                               RemindParticipantsView, )

urlpatterns = [
    path(
        'participants/',
        ExperimentAppointmentsView.as_view(),
        name='participants',
    ),

    path(
        'participants/remind/',
        RemindParticipantsView.as_view(),
        name='remind_participants',
    ),

    path(
        'invite/',
        InviteParticipantsForExperimentView.as_view(),
        name='invite',
    ),

    path(
        'invite/preview/',
        InviteEmailPreview.as_view(),
        name='mail_preview',
    ),
]
