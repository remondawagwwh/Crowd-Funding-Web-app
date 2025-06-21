from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # dj-rest-auth endpoints
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # allauth URLs (لربط التطبيق بـ Facebook من admin)
    path('api/auth/social/', include('allauth.socialaccount.urls')),

    # custom user views (فيها FacebookLogin مثلاً)
    path('api/auth/', include('users.urls')),

    # other apps
    path('api/comment/', include('comment_app.urls')),
]
