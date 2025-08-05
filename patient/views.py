from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConditionSerializer, MedicationSerializer, PatientSerializer, RadiographSerializer, ToothTreatmentSerializer
from .models import Medication, Patient, Radiograph, ToothTreatment
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from django.http import HttpResponse


from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_str

from .models import Patient
from .models import Patient, Condition


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # الطبيب يجب أن يكون مسجلاً للدخول
def addPatientToDoctor(request):
    serializer = PatientSerializer(
        data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()  # يتم استدعاء create() داخل السيريالايزر وربط الطبيب تلقائيًا
        return Response({'details': 'تم إضافة المريض بنجاح'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addMedicationToPatient(request, patient_id):
    try:
        # تأكد أن المريض للطبيب الحالي
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['patient'] = patient.id  # ربط الدواء بالمريض

    serializer = MedicationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'details': 'تم إضافة الدواء بنجاح'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addTreatmentToPatient(request, patient_id):
    try:
        # التأكد من أن المريض موجود ويتبع الطبيب الحالي
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['patient'] = patient.id  # ربط العلاج بالمريض

    serializer = ToothTreatmentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'details': 'تم إضافة العلاج بنجاح'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addRadiographToPatient(request, patient_id):
    try:
        # التأكد أن المريض موجود ويتبع هذا الطبيب
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['patient'] = patient.id  # ربط الأشعة بالمريض

    serializer = RadiographSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'details': 'تم إضافة الأشعة بنجاح'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # الطبيب يجب أن يكون مسجلاً للدخول
def addPatientWithAllData(request):
    serializer = PatientSerializer(
        data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()  # سيتم إنشاء المريض وربطه بالطبيب مع كل عناصره
        return Response({'details': 'تم إضافة المريض بكامل البيانات بنجاح'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_patients_for_current_doctor(request):
    doctor = request.user
    patients = Patient.objects.filter(doctor=doctor).order_by(
        '-id')  # عرض المرضى الأحدث أولًا
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_patient(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    patient.delete()
    return Response({'details': 'تم حذف المريض بنجاح'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medication_from_patient(request, patient_id, medication_id):
    try:
        # تأكد أن المريض يتبع هذا الطبيب
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # تأكد أن الدواء يتبع هذا المريض
        medication = Medication.objects.get(id=medication_id, patient=patient)
    except Medication.DoesNotExist:
        return Response({'error': 'الدواء غير موجود أو لا يتبع هذا المريض'}, status=status.HTTP_404_NOT_FOUND)

    medication.delete()
    return Response({'details': 'تم حذف الدواء بنجاح'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_treatment_from_patient(request, patient_id, treatment_id):
    try:
        # تأكد من أن المريض يتبع الطبيب الحالي
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # تأكد أن العلاج يتبع هذا المريض
        treatment = ToothTreatment.objects.get(
            id=treatment_id, patient=patient)
    except ToothTreatment.DoesNotExist:
        return Response({'error': 'العلاج غير موجود أو لا يتبع هذا المريض'}, status=status.HTTP_404_NOT_FOUND)

    treatment.delete()
    return Response({'details': 'تم حذف العلاج بنجاح'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_radiograph_from_patient(request, patient_id, radiograph_id):
    try:
        # التأكد أن المريض يتبع الطبيب الحالي
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # التأكد أن الأشعة تتبع هذا المريض
        radiograph = Radiograph.objects.get(id=radiograph_id, patient=patient)
    except Radiograph.DoesNotExist:
        return Response({'error': 'الأشعة غير موجودة أو لا تتبع هذا المريض'}, status=status.HTTP_404_NOT_FOUND)

    # حذف الأشعة
    radiograph.delete()
    return Response({'details': 'تم حذف الأشعة بنجاح'}, status=status.HTTP_204_NO_CONTENT)


###################################

def safe_get(obj, attr, default="غير متوفر"):
    return getattr(obj, attr, default) or default


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_patient_pdf(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, doctor=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="patient_{patient_id}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    y = 800
    p.drawString(50, y, f"اسم المريض: {safe_get(patient, 'name')}")
    y -= 20
    p.drawString(50, y, f"العمر: {safe_get(patient, 'age')}")
    y -= 20
    p.drawString(50, y, f"الجنس: {safe_get(patient, 'gender')}")
    y -= 20
    p.drawString(50, y, f"رقم الهاتف: {safe_get(patient, 'phone')}")
    y -= 20
    p.drawString(50, y, f"العنوان: {safe_get(patient, 'address')}")
    y -= 20
    p.drawString(
        50, y, f"تاريخ الأسنان: {safe_get(patient, 'dental_history')}")

    p.showPage()
    p.save()
    return response


############################
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_radiograph_from_patient(request, patient_id, radiograph_id):
    try:
        # التأكد أن المريض يتبع الطبيب الحالي
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # التأكد أن الأشعة تتبع هذا المريض
        radiograph = Radiograph.objects.get(id=radiograph_id, patient=patient)
    except Radiograph.DoesNotExist:
        return Response({'error': 'الأشعة غير موجودة أو لا تتبع هذا المريض'}, status=status.HTTP_404_NOT_FOUND)

    # حذف الأشعة
    radiograph.delete()
    return Response({'details': 'تم حذف الأشعة بنجاح'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_radiograph_image_to_patient(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['patient'] = patient.id  # ربط الأشعة بالمريض

    serializer = RadiographSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'تم إضافة صورة الأشعة بنجاح'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 7 /31 /20225
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_patient_phone(request, patient_id):
    try:
        # التأكد أن المريض يتبع الطبيب الحالي
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    new_phone = request.data.get('phone')
    if not new_phone:
        return Response({'error': 'يرجى إرسال رقم الهاتف الجديد في الطلب'}, status=status.HTTP_400_BAD_REQUEST)

    patient.phone = new_phone
    patient.save()

    return Response({'details': 'تم تحديث رقم الهاتف بنجاح'}, status=status.HTTP_200_OK)


#############
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_condition_to_patient(request, patient_id):
#     try:
#         # التأكد أن المريض يتبع الطبيب الحالي
#         patient = Patient.objects.get(id=patient_id, doctor=request.user)
#     except Patient.DoesNotExist:
#         return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

#     data = request.data.copy()
#     data['patient'] = patient.id  # ربط الحالة بالمريض

#     serializer = ConditionSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'details': 'تم إضافة الحالة بنجاح'}, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_condition_to_patient(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    # التعامل مع أنواع مختلفة من البيانات
    if hasattr(request.data, 'getlist'):
        conditions = request.data.getlist('conditions')
    else:
        cond = request.data.get('conditions')
        if isinstance(cond, list):
            conditions = cond
        elif isinstance(cond, str):
            conditions = [cond]
        else:
            return Response({'error': 'يرجى إرسال الحالات كنص أو قائمة نصوص'}, status=400)

    if not conditions:
        return Response({'error': 'يرجى إرسال الحقول المطلوبة'}, status=status.HTTP_400_BAD_REQUEST)

    for cond in conditions:
        Condition.objects.create(patient=patient, name=cond)

    return Response({'message': 'تمت إضافة الحالات بنجاح'}, status=status.HTTP_201_CREATED)
