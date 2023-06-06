
from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, RegisterPage

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout'),
    path('sign-up/', RegisterPage.as_view(), name = 'sign-up'),
]
