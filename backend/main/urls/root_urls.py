from django.urls import path
from django.contrib.auth import views as auth_views

from ..views import HomeView

class LegacyLogoutView(auth_views.LogoutView):
    """Temporary workaround for django deperecating logout via GET"""
    http_method_names = ["get"]
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LegacyLogoutView.as_view(), name='logout'),
]
