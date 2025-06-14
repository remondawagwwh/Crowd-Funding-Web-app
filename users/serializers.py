from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import MyUser
from django.contrib.auth.password_validation import validate_password
import re


class MyUser_ser(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields = ['id', 'first_name', 'last_name', 'email', 'mobile_phone', 'profile_picture', 'birthdate',
                  'facebook_profile', 'country', 'is_active']

    @classmethod
    def getall(cls):
        return  cls(MyUser.getalluser(),
                    many=True).data
    @classmethod
    def getbyid(cls,id):
        return  MyUser_ser(MyUser.getuserbyid(id)).data


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password',
                  'mobile_phone', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_mobile_phone(self, value):
        if not re.match(r'^01[0125][0-9]{8}$', value):
            raise ValidationError("Phone number must be Egyptian and in the format: '01XXXXXXXXX'.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        if MyUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        if MyUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = MyUser.objects.create_user(**validated_data)
        user.generate_activation_token()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])  # أو email حسب إعداداتك
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise serializers.ValidationError("Account not activated. Please check your email.")

        return {'user': user}



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = MyUser.objects.get(email=value)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError("User with this email doesn't exist.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True,validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'email', 'username', 'first_name', 'last_name', 'mobile_phone',
            'profile_picture', 'birthdate', 'facebook_profile', 'country'
        ]
        read_only_fields = ['email']

class AccountDeleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)