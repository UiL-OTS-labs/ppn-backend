from django.urls import path

from experiments.views import (ExperimentCreateView,
                               ExperimentDeleteView,
                               ExperimentDetailView,
                               ExperimentEmailTemplatesUpdateView,
                               ExperimentHomeView,
                               ExperimentUpdateView,
                               )

urlpatterns = [
    path('', ExperimentHomeView.as_view(), name='home'),
    path('new/', ExperimentCreateView.as_view(), name='create'),
    path('<int:pk>/', ExperimentDetailView.as_view(), name='detail'),
    path('<int:pk>/emails/', ExperimentEmailTemplatesUpdateView.as_view(),
         name='email_templates'),
    path('<int:pk>/update/', ExperimentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ExperimentDeleteView.as_view(),
         name='delete'),
]
