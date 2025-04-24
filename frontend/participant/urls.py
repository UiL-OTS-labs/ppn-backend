from django.urls import include, path

from participant.views import AccountCreatedView, AuthenticatedRegisterView, \
    CancelAppointmentView, CancelLandingView, ClosedExperimentView, \
    MyAppointmentsView, RegisterSuccessView, RegisterView, SubscribedView, \
    UnsubscribeFromMailinglistView, SignUpView

app_name = 'participant'

urlpatterns = [
    path('register/<int:experiment>/', RegisterView.as_view(), name='register'),
    path(
        'secure/register/<int:experiment>/',
        AuthenticatedRegisterView.as_view(),
        name='register_logged_in'
    ),
    path('register/<int:experiment>/success/', RegisterSuccessView.as_view(),
         name='register_success'),

    path('closed/', ClosedExperimentView.as_view(), name='closed_experiment'),
    path('cancel/', include([
        path('', CancelLandingView.as_view(), name='cancel_landing'),
    ])),

    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('sign_up/account_created/', AccountCreatedView.as_view(),
         name='sign_up_account_created'),
    path('sign_up/subscribed/', SubscribedView.as_view(),
         name='sign_up_subscribed'),

    path(
        'unsubscribe_mailinglist/<str:token>/',
        UnsubscribeFromMailinglistView.as_view(),
        name='unsubscribe_mailinglist'
    ),

    path('appointments/', MyAppointmentsView.as_view(), name='appointments'),
    path(
        'appointments/<str:token>/',
        MyAppointmentsView.as_view(),
        name='appointments'
    ),
    path(
        'appointments/<int:appointment>/cancel/',
        CancelAppointmentView.as_view(),
        name='cancel_appointment'
    ),
    path(
        'appointments/<str:token>/<int:appointment>/cancel/',
        CancelAppointmentView.as_view(),
        name='cancel_appointment'
    ),
]
