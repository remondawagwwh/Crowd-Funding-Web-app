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


# CRUD ViewSet for Users
class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUser_ser


@api_view(['POST'])
@permission_classes([AllowAny])
def UserRegistrationView(request):
    userobj = UserRegistrationSerializer(data=request.data)
    if userobj.is_valid():
        user=userobj.save()
        subject = 'Activate Your Account'
        message=render_to_string('users/verification_email.html',{
            'user':user,
            'domain':request.get_host(),
            'uid':urlsafe_base64_decode(force_bytes(user.pk)),
            'token':user.activation_token
        })
        # Send activation email
        send_mail(subject,message,'noreply@charity.com',[user.email])
        return Response(data=userobj.data,   status=status.HTTP_201_CREATED )
    else:
        return Response(data={'errors':userobj.errors},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def verify_email(request, uid, token):
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = get_object_or_404(MyUser, pk=uid_decoded)
    except (user.DoesNotExist, ValueError, TypeError, OverflowError):
        return Response({'msg': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

    if user.check_activation_token(token):
        return Response({'msg': 'Email confirmed'}, status=status.HTTP_200_OK)
    else:
        return Response({'msg': 'Invalid or expired token'}, status=status.HTTP_406_NOT_ACCEPTABLE)