from rest_framework import serializers
from .models import Patient, Medication, ToothTreatment, Radiograph, Condition
from django.contrib.auth.models import User
from Ai.serializers import AnalysisReportSerializer


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'
        extra_kwargs = {'patient': {'required': False}}


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'
        extra_kwargs = {'patient': {'required': False}}


class ToothTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToothTreatment
        fields = '__all__'
        extra_kwargs = {'patient': {'required': False}}


class RadiographSerializer(serializers.ModelSerializer):
    class Meta:
        model = Radiograph
        fields = '__all__'
        extra_kwargs = {'patient': {'required': False}}


class PatientSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField()  # عرض اسم الطبيب

    medications = MedicationSerializer(many=True, required=False)
    treatments = ToothTreatmentSerializer(many=True, required=False)
    radiographs = RadiographSerializer(many=True, required=False)
    analysis_reports = AnalysisReportSerializer(
        many=True, required=False)  # أضف هذا
    conditions = ConditionSerializer(
        many=True, required=False)  # أضف هذا السطر
    
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {
            'doctor': {'read_only': True}
        }

    def create(self, validated_data):
        medications_data = validated_data.pop('medications', [])
        treatments_data = validated_data.pop('treatments', [])
        radiographs_data = validated_data.pop('radiographs', [])

        # تعيين الطبيب من السياق (request.user)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['doctor'] = request.user

        patient = Patient.objects.create(**validated_data)

        for medication_data in medications_data:
            Medication.objects.create(patient=patient, **medication_data)

        for treatment_data in treatments_data:
            ToothTreatment.objects.create(patient=patient, **treatment_data)

        for radiograph_data in radiographs_data:
            Radiograph.objects.create(patient=patient, **radiograph_data)

        return patient
