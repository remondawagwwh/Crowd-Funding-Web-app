from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from .models import MyUser
from .serializers import (
    MyUser_ser,
    UserRegistrationSerializer,
    UserLoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer
)
from django.http import JsonResponse

class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUser_ser


@api_view(['POST'])
@permission_classes([AllowAny])
def UserRegistrationView(request):
    userobj = UserRegistrationSerializer(data=request.data)
    if userobj.is_valid():
        user = userobj.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = settings.MY_DOMAIN
        html_message = render_to_string('users/verification_email.html', {
            'user': user,
            'domain': domain,
            'uid': uid,
            'token': user.activation_token
        })
        plain_message = strip_tags(html_message)
        email = EmailMultiAlternatives('Activate Your Account', plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email.attach_alternative(html_message, "text/html")
        email.send()
        return Response(userobj.data, status=status.HTTP_201_CREATED)
    return Response({'errors': userobj.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, uid, token):
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = get_object_or_404(MyUser, pk=uid_decoded)
    except Exception:
        return Response({'msg': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

    if user.check_activation_token(token):
        user.is_active = True
        user.save()
        return Response({'msg': 'Email confirmed successfully. You can now login.'}, status=status.HTTP_200_OK)
    return Response({'msg': 'Invalid or expired token'}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@permission_classes([AllowAny])
def UserLoginView(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        user_data = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': token.key,
        }
        return Response({'msg': 'Login successful', 'user': user_data, 'token': token.key}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_request(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = MyUser.objects.get(email=serializer.validated_data['email'])
        token = user.generate_reset_token()
        message = render_to_string('users/reset_password_email.html', {
            'user': user,
            'domain': request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token
        })
        send_mail('Password Reset Request', message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return Response({'message': 'Password reset email sent.'}, status=200)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request, uid, token):
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = MyUser.objects.get(pk=uid_decoded)
    except (MyUser.DoesNotExist, ValueError, TypeError, OverflowError):
        return Response({'msg': 'Invalid link'}, status=400)

    if not user.check_reset_token(token):
        return Response({'msg': 'Invalid or expired token'}, status=400)

    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        user.set_password(serializer.validated_data['new_password'])
        user.reset_token = ''
        user.reset_token_expires = None
        user.save()
        return Response({'msg': 'Password reset successful'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    password = request.data.get("password")
    if not password:
        return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
    if not user.check_password(password):
        return Response({'error': 'Incorrect password'}, status=status.HTTP_403_FORBIDDEN)
    user.delete()
    return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
    except Exception:
        return Response({'error': 'Token not found or already deleted.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


def account_inactive_view(request):
    return JsonResponse({"detail": "Your account is inactive. Please contact support."}, status=403)
