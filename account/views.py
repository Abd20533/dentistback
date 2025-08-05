from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SinUpSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import random
from django.utils.timezone import now
from django.utils import timezone
from .models import profile
from .serializers import ProfileSerializer  # سننشئ هذا لاحقاً
from rest_framework.decorators import action

@api_view(['POST'])
def register(request):
    data = request.data
    photo = request.FILES.get('photo')

    user_serializer = SinUpSerializer(data=data)
    if user_serializer.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                username=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password=make_password(data['password'])
            )
            # Set the profile photo
            if photo:
                user.profile.photo = photo
            user.profile.save()

            return Response({'details': 'Your account registered successfully'},
                            status=status.HTTP_201_CREATED)

        else:
            return Response({'error': 'This email already exists'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data
    photo = request.FILES.get('photo')

    # Update user fields
    if 'email' in data:
        user.email = data['email']
        user.username = data['email']

    user.save()

    # Update profile photo if provided
    if photo:
        user.profile.photo = photo
        user.profile.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    data = request.data

    if 'new_password' in data and data['new_password'].strip() != "":
        old_password = data.get('old_password', '').strip()
        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect."}, status=400)

        user.password = make_password(data['new_password'])

    user.save()
    return Response({"detail": "your password changed successfully."}, status=200)


def get_current_host(request):

    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


@api_view(['POST'])
def forget_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])

    # Generate a random 5-digit code
    code = str(random.randint(10000, 99999))
    expire_date = now() + timedelta(minutes=30)

    user.profile.reset_password_token = code
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    # Email content
    body = f"Your password reset code is: {code}"

    send_mail(
        "Password Reset Code",
        body,
        "dentistai404@gmail.com",
        [data['email']]
    )

    return Response({'detail': f'Password reset code sent to {data["email"]}'})


@api_view(['POST'])
def reset_password(request):
    data = request.data

    code = data.get('code')
    if not code:
        return Response({'error': 'Reset code is required'}, status=400)

    user = get_object_or_404(User, profile__reset_password_token=code)

    # Check if the code expired
    if user.profile.reset_password_expire < timezone.now():
        return Response({'error': 'Reset code has expired'}, status=400)
    # Check password match
    if data['password'] != data['confirm_password']:
        return Response({'error': 'Passwords do not match'}, status=400)

    # Reset password
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.save()
    user.profile.save()

    return Response({'detail': 'Password has been reset successfully'})



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def doctor_patients(request):
#     # استرجاع جميع مرضى الطبيب الحالي
#     patients = Patient.objects.filter(doctor=request.user)
#     serializer = PatientSerializer(patients, many=True)
#     return Response(serializer.data)

