from django.urls import path

from .views import HideParticipantsView, OverviewView, DeleteInvitesView, \
    DeleteCommentsView, ThresholdsEditView, DeleteParticipantView, AnonymizeParticipantView\
     , BulkAnonymizeView, BulkDeleteView

app_name = 'datamanagement'

urlpatterns = [
    path('', OverviewView.as_view(), name='overview'),
    path('edit_thresholds/', ThresholdsEditView.as_view(), name='thresholds'),

    path('<int:participant>/delete/',
         DeleteParticipantView.as_view(),
         name="delete_participant"),
    path('<int:participant>/anonymize/', 
         AnonymizeParticipantView.as_view(),
         name="anonymize_participant"),
    path('<int:experiment>/hide_participants/',
         HideParticipantsView.as_view(),
         name='hide_participants'),
    path('<int:experiment>/delete_invites/',
         DeleteInvitesView.as_view(),
         name='delete_invites'),
    path('<int:experiment>/delete_comments/',
         DeleteCommentsView.as_view(),
         name='delete_comments'),
    path('bulk_anonymize/', 
         BulkAnonymizeView.as_view(), name='bulk_anonymize'),
    path('bulk_delete/', 
         BulkDeleteView.as_view(), name='bulk_delete'),
]
