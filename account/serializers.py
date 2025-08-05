# from rest_framework import serializers
# from django.contrib.auth.models import User
# # في account/serializers.py
# from patient.serializers import PatientSerializer  # إذا كان التطبيق اسمه patient

# class SinUpSerializer (serializers.ModelSerializer):
#     class Meta :
#         model = User
#         fields = ('first_name','last_name','email','password')
#         extra_kwargs ={
#             'first_name': {'required':True ,'allow_blank':False},
#             'last_name': {'required':True ,'allow_blank':False},
#             'email': {'required':True ,'allow_blank':False},
#             'password': {'required':True ,'allow_blank':False , 'min_length':8}
#         }

# class UserSerializer(serializers.ModelSerializer):
#     photo = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'username', 'photo')

#     def get_photo(self, obj):
#         if hasattr(obj, 'profile') and obj.profile.photo:
#             return obj.profile.photo.url
#         return None


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import profile
from patient.serializers import PatientSerializer  # استيراد سيريالايزر المريض


class SinUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8}
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = ['reset_password_token', 'reset_password_expire', 'photo']


class UserSerializer(serializers.ModelSerializer):
    # حقل الصورة (من النسخة الأصلية)
    photo = serializers.SerializerMethodField()

    # حقل المرضى (من الاقتراح الجديد)
    patients = PatientSerializer(many=True, read_only=True)

    # بيانات الملف الشخصي
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'photo',
            'patients',
            'profile'
        )

    def get_photo(self, obj):
        """دالة للحصول على رابط الصورة"""
        # استخدم related_name 'profile' للوصول لصورة الملف الشخصي
        if hasattr(obj, 'profile') and obj.profile.photo:
            # بناء رابط كامل للصورة
            request = self.context.get('request')
            photo_url = obj.profile.photo.url
            if request is not None:
                return request.build_absolute_uri(photo_url)
            return photo_url
        return None
