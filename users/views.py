from rest_framework import  viewsets
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import MyUser
from django.template.loader import render_to_string
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site


# CRUD ViewSet for Users
class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUser_ser



@api_view(['POST'])
@permission_classes([AllowAny])
def UserRegistrationView(request):
    userobj = UserRegistrationSerializer(data=request.data)
    if userobj.is_valid():
        user = userobj.save()

        subject = 'Activate Your Account'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        message = render_to_string('users/verification_email.html', {
            'user': user,
            'domain': domain,
            'uid': uid,
            'token': user.activation_token
        })

        send_mail(subject, message, 'noreply@charity.com', [user.email])
        return Response(data=userobj.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data={'errors': userobj.errors}, status=status.HTTP_400_BAD_REQUEST)


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
    else:
        return Response({'msg': 'Invalid or expired token'}, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@permission_classes([AllowAny])
def UserLoginView(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        user_data = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response({'msg': 'Login successful', 'user': user_data}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_request(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = MyUser.objects.get(email=serializer.validated_data['email'])
        token = user.generate_reset_token()

        subject = "Password Reset Request"
        message = render_to_string('users/reset_password_email.html', {
            'user': user,
            'domain': request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token
        })

        send_mail(subject, message, 'noreply@charity.com', [user.email])

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
        return Response({'msg': 'Password reset successful'}, status=200)

    return Response(serializer.errors, status=400)

