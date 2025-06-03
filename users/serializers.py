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
    password = serializers.CharField(write_only=True, required=True,validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password',
                  'mobile_phone', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def validate_mobile_phone(self, value):
        if not re.match(r'^01[0125][0-9]{8}$', value):
            raise ValidationError("Phone number must be Egyptian and in the format: '01XXXXXXXXX'.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        # Check if email already exists
        if MyUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        # Check if username already exists
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
        user = authenticate(email=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise serializers.ValidationError("Account not activated. Please check your email.")

        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    email = serializers.EmailField()

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'mobile_phone',
                  'profile_picture', 'birthdate', 'facebook_profile', 'country']
        read_only_fields = ['email']

class AccountDeleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)