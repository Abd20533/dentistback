from attr import fields
from rest_framework import serializers as ser
from django.contrib.auth.models import User


class SignUpSerializer  (ser.ModelSerializer):
    class Meta:
        model = User
        fields=('first_name','last_name',"email","password")
        extra_kwargs = {

            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
        }


class UserSerializers(ser.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
