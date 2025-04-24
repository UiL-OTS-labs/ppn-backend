from django.contrib.auth import views as auth_views
from django.urls import path

from .views import ChangePasswordView, CustomLoginView, EnterTokenView, \
    ForgotPasswordView, HomeApiView, HomeView, PrivacyView, ResetPasswordView, \
    LDAPPasswordView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('api/experiments/', HomeApiView.as_view(), name='home_api'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('change_password/ldap/', LDAPPasswordView.as_view(),
         name='ldap_password'),

    path('change_password/', ChangePasswordView.as_view(),
         name='change_password'),
    path('forgot_password/', ForgotPasswordView.as_view(),
         name='forgot_password'),
    path('reset_password/<str:token>/', ResetPasswordView.as_view(),
         name='reset_password'),
    path('reset_password/', EnterTokenView.as_view(),
         name='enter_token'),

]
