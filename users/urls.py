from django.urls import path, include
from .views import (
    UserRegistrationView,
    verify_email,
    UserLoginView,
    forgot_password_request,
    reset_password,
    user_profile,
    delete_account,
    FacebookLogin,
    UserViewSet,

)


urlpatterns = [
    path('users/', UserViewSet, name='AllUser'),
    path('register/', UserRegistrationView, name='register'),
    path('activate/<uid>/<token>/', verify_email, name='activate'),
    path('login/', UserLoginView, name='user-login'),
    path('forgot-password/', forgot_password_request, name='forgot-password'),
    path('reset-password/<str:uid>/<str:token>/', reset_password, name='reset-password'),
    path('profile/', user_profile, name='user-profile'),
    path('profile/delete/', delete_account, name='delete-account'),
    path('auth/social/', include('allauth.socialaccount.urls')),
    path('auth/', include('dj_rest_auth.registration.urls')),
    path('auth/social/facebook/', FacebookLogin.as_view(), name='fb_login'),

]




