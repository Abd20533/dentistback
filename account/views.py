from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializer

@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)
    if user.is_valid() :
        if   User.objects.filter(username=data['email']).exists():
            return Response({"error": "__this email already exists__"}, status=status.HTTP_400_BAD_REQUEST)
        print("12345")
        user = User.objects.create(
            username=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=make_password(data["password"]),
        )
        print("54321")
        return Response(
            {
                'details':'registered successfully!'
                },
            status=status.HTTP_201_9CREATED)

    else:
        print(user.errors)
        return Response({"error__register": user.errors}, status=status.HTTP_400_BAD_REQUEST)
#LHGFDSDFGHKJHGF