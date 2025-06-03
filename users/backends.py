# accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import MyUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email', username)
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
