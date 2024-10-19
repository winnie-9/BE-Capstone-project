from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('accounts/register/', RegisterView.as_view(), name='accounts_register'),
    path('accounts/login/', LoginView.as_view(), name='accounts_login'),
]