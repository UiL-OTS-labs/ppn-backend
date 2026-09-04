from django.contrib.auth import views as auth_views
from django.urls import path

from .views import ChangePasswordView, CustomLoginView, EnterTokenView, \
    ForgotPasswordView, HomeView, PrivacyView, ResetPasswordView, \
    LDAPPasswordView

app_name = 'main'

class LegacyLogoutView(auth_views.LogoutView):
    """Temporary workaround for django deperecating logout via GET"""
    http_method_names = ["get"]
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LegacyLogoutView.as_view(), name='logout'),

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
