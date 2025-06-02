from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404


class MyUser(AbstractUser ,PermissionsMixin):
    # Disable username and use email instead
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    # Required fields
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)


    mobile_phone = models.CharField(
        validators=[RegexValidator(
        regex=r'^01[0125][0-9]{8}$',
        message="Phone number must be Egyptian and in the format: '01XXXXXXXXX'."
    )],
        max_length=11,
        unique=True
    )

    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Optional fields
    birthdate = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    # Activation fields
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=100, blank=True)
    activation_token_expires = models.DateTimeField(null=True, blank=True)

    # Field to use as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'mobile_phone']

    def generate_activation_token(self):
        self.activation_token = get_random_string(50)
        self.activation_token_expires = timezone.now() + timezone.timedelta(hours=24)
        self.save()
        return self.activation_token

    def check_activation_token(self, token):
        if (self.activation_token == token and
                self.activation_token_expires and
                timezone.now() < self.activation_token_expires):
            self.is_active = True
            self.activation_token = ''
            self.activation_token_expires = None
            self.save()
            return True
        return False

    @classmethod
    def getalluser(cls):
        return cls.objects.filter(Active=True)

    @classmethod
    def getuserbyid(cls, id):
        return get_object_or_404(cls, id=id)

    def __str__(self):
        return self.email