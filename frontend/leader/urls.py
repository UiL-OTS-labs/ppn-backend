from django.urls import path

from .views import AddCommentView, DeleteAppointmentView, \
    DownloadParticipantsCsvView, ExperimentParticipantsView, ExperimentsView, \
    ProfileView, RemindParticipantsView, SwitchExperimentOpenView, \
    TimeSlotBulkDeleteView, \
    TimeSlotDeleteView, TimeSlotHomeView

app_name = 'leader'

urlpatterns = [
    path('', ExperimentsView.as_view(), name='experiments'),
    path('experiment/<int:experiment>/switch_open',
         SwitchExperimentOpenView.as_view(), name='experiment_switch_open'),

    path('experiment/<int:experiment>/timeslots/',
         TimeSlotHomeView.as_view(), name='timeslots',
         ),

    path('experiment/<int:experiment>/participants/',
         ExperimentParticipantsView.as_view(), name='participants',
         ),

    path('experiment/<int:experiment>/participants/send_reminders/',
         RemindParticipantsView.as_view(), name='send_reminders',
         ),

    path('experiment/<int:experiment>/participants/download/',
         DownloadParticipantsCsvView.as_view(), name='download_csv',
         ),

    path('experiment/<int:experiment>/participants/<int:participant'
         '>/add_comment/',
         AddCommentView.as_view(), name='add_comment',
         ),

    path('experiment/<int:experiment>/timeslots/<int:timeslot>/delete/',
         TimeSlotDeleteView.as_view(), name='delete_timeslot'),

    path('experiment/<int:experiment>/timeslots/appointments/<int:appointment'
         '>/delete/',
         DeleteAppointmentView.as_view(), name='delete_appointment'),

    path('experiment/<int:experiment>/timeslots/delete/',
         TimeSlotBulkDeleteView.as_view(), name='delete_timeslots'),

    path('profile/', ProfileView.as_view(), name='profile'),
]
