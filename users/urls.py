from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView, name='register'),
    path('activate/<uid>/<token>/', verify_email, name='activate'),
    path('login/', UserLoginView, name='user-login'),
    path('forgot-password/', forgot_password_request, name='forgot-password'),
    path('reset-password/<str:uid>/<str:token>/', reset_password, name='reset-password'),
]
