# # # AI/views.py
# # from rest_framework.decorators import api_view, permission_classes
# # from rest_framework.permissions import IsAuthenticated
# # from rest_framework.response import Response
# # from rest_framework import status
# # from django.conf import settings
# # import os
# # import uuid

# # from patient.models import Patient, Radiograph  # أو موديل التحليل الخاص بك
# # from patient.serializers import RadiographSerializer
# # from .ai_engine import AdvancedDentalAnalysis

# # @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# # def analyze_image_for_patient(request, patient_id):
# #     try:
# #         # تأكد من أن المريض يتبع هذا الطبيب
# #         patient = Patient.objects.get(id=patient_id, doctor=request.user)
# #     except Patient.DoesNotExist:
# #         return Response({'error': 'المريض غير موجود أو لا يتبع هذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

# #     image_file = request.FILES.get('image')
# #     if not image_file:
# #         return Response({'error': 'لم يتم إرسال صورة'}, status=status.HTTP_400_BAD_REQUEST)

# #     # حفظ مؤقت للصورة
# #     temp_name = f"{uuid.uuid4().hex}.jpg"
# #     temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', temp_name)
# #     os.makedirs(os.path.dirname(temp_path), exist_ok=True)

# #     with open(temp_path, 'wb+') as f:
# #         for chunk in image_file.chunks():
# #             f.write(chunk)

# #     try:
# #         analyzer = AdvancedDentalAnalysis(
# #             detection_model_path=os.path.join(settings.BASE_DIR, 'AI/models/best.pt'),
# #             classification_model_path=os.path.join(settings.BASE_DIR, 'AI/models/tooth_model2.h5')
# #         )
# #         results = analyzer.detect_and_classify(temp_path)
# #         report = analyzer.generate_report(results)

# #         # حذف الصورة المؤقتة بعد التحليل
# #         os.remove(temp_path)

# #         # (اختياري) يمكنك حفظ الأشعة أو التحليل كموديل Radiograph
# #         # مثلاً حفظ الصورة أو نتائج التوصيف
# #         # Radiograph.objects.create(patient=patient, image=...)

# #         return Response({
# #             'details': 'تم تحليل الصورة بنجاح',
# #             'summary': report['summary'],
# #             'results': report['detailed_findings']
# #         }, status=status.HTTP_200_OK)

# #     except Exception as e:
# #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# # AI/views.py
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
# import os
# import uuid

# from .ai_engine import AdvancedDentalAnalysis

# @api_view(['POST'])
# def analyze_image(request):
#     image_file = request.FILES.get('image')
#     if not image_file:
#         return Response({'error': 'لم يتم إرسال صورة'}, status=status.HTTP_400_BAD_REQUEST)

#     # حفظ الصورة مؤقتاً
#     temp_name = f"{uuid.uuid4().hex}.jpg"
#     temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', temp_name)
#     os.makedirs(os.path.dirname(temp_path), exist_ok=True)
#     with open(temp_path, 'wb+') as f:
#         for chunk in image_file.chunks():
#             f.write(chunk)

#     try:
#         analyzer = AdvancedDentalAnalysis(
#             "E:\django\dentist\project\model\best.pt"
#             "E:\django\dentist\project\model\tooth_model.h5"
#             detection_model_path=os.path.join(settings.BASE_DIR, 'AI', 'models', 'best.pt'),
#             classification_model_path=os.path.join(settings.BASE_DIR, 'AI', 'models', 'tooth_model2.h5')
#         )
#         results = analyzer.detect_and_classify(temp_path)
#         report = analyzer.generate_report(results)

#         # حذف الصورة المؤقتة بعد التحليل
#         os.remove(temp_path)

#         return Response({
#             'summary': report['summary'],
#             'details': report['detailed_findings'],
#         }, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# AI/views.py
from .models import AnalysisReport, Finding
from patient.models import Patient
import uuid, os, cv2
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
import uuid
from patient.models import Radiograph

from .ai_engine import AdvancedDentalAnalysis

# AI/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os
import uuid
import base64
import cv2
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import AnalysisReport
from .serializers import AnalysisReportSerializer

from .ai_engine import AdvancedDentalAnalysis


@api_view(['POST'])
def analyze_image1(request):
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({'error': 'لم يتم إرسال صورة'}, status=status.HTTP_400_BAD_REQUEST)

    # حفظ الصورة مؤقتاً
    temp_name = f"{uuid.uuid4().hex}.jpg"
    temp_path = f"E:/django/dentist/media/temp/{temp_name}"
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)

    with open(temp_path, 'wb+') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    try:
        analyzer = AdvancedDentalAnalysis(
            detection_model_path="E:/django/dentist/project/model/best.pt",
            classification_model_path="E:/django/dentist/project/model/tooth_model.h5"
        )

        results = analyzer.detect_and_classify(temp_path)
        report = analyzer.generate_report(results)

        # حذف الصورة المؤقتة بعد التحليل
        os.remove(temp_path)

        return Response({
            'summary': report['summary'],
            'details': report['detailed_findings'],
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ممهم


@api_view(['POST'])
def analyze_image2(request):
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({'error': 'لم يتم إرسال صورة'}, status=status.HTTP_400_BAD_REQUEST)

    # حفظ الصورة مؤقتاً
    temp_name = f"{uuid.uuid4().hex}.jpg"
    temp_path = f"E:/django/dentist/media/temp/{temp_name}"
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)

    with open(temp_path, 'wb+') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    try:
        analyzer = AdvancedDentalAnalysis(
            detection_model_path="E:/django/dentist/project/model/best.pt",
            classification_model_path="E:/django/dentist/project/model/tooth_model.h5"
        )

        results = analyzer.detect_and_classify(temp_path)
        report = analyzer.generate_report(results)

        # تحويل الصورة الملونة المعلّمة إلى صيغة Base64
        annotated_img = report['visualization']
        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        # حذف الصورة المؤقتة بعد التحليل
        os.remove(temp_path)

        return Response({
            'summary': report['summary'],
            'details': report['detailed_findings'],
            'annotated_image_base64': img_base64,  # هنا الصورة الملونة مشفرة Base64
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ممهم  ثثثثثثثثثثثثثثثثثثثثثثثثثثثثثثثثثثثثثث


@api_view(['POST'])
def analyze_image3(request):
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({'error': 'لم يتم إرسال صورة'}, status=status.HTTP_400_BAD_REQUEST)

    # حفظ الصورة الأصلية مؤقتًا
    temp_name = f"{uuid.uuid4().hex}.jpg"
    temp_path = f"E:/django/dentist/media/temp/{temp_name}"
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)

    with open(temp_path, 'wb+') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    try:

        analyzer = AdvancedDentalAnalysis(
            detection_model_path="E:/django/dentist/project/model/best.pt",
            classification_model_path="E:/django/dentist/project/model/tooth_model.h5"
        )

        results = analyzer.detect_and_classify(temp_path)
        report = analyzer.generate_report(results)

        # الصورة المعلّمة (annotated image)
        annotated_img = report['visualization']

        # حفظ الصورة المعالجة (annotated image) في مجلد محدد
        annotated_name = f"annotated_{uuid.uuid4().hex}.jpg"
        annotated_path = f"E:/django/dentist/media/annotated/{annotated_name}"
        os.makedirs(os.path.dirname(annotated_path), exist_ok=True)
        cv2.imwrite(annotated_path, annotated_img)

        # حذف الصورة الأصلية المؤقتة بعد الانتهاء
        os.remove(temp_path)

        # بناء رابط الوصول للصورة المعلّمة (يمكن تعديله حسب إعدادات الـ MEDIA_URL في Django)
        # مثلاً إذا الـMEDIA_URL = '/media/', نرسل المسار النسبي
        relative_path = f"/media/annotated/{annotated_name}"

        return Response({
            'summary': report['summary'],
            'details': report['detailed_findings'],
            'annotated_image_path': relative_path,  # نرسل مسار الصورة وليس Base64
        }, status=status.HTTP_200_OK)

    except Exception as e:
        # حذف الصورة الأصلية لو حدث خطأ (تجنب تراكم الملفات)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# def analyze_image(request):
#     image_file = request.FILES.get('image')
#     if not image_file:
#         return Response({'error': 'لم يتم إرسال صورة'}, status=status.HTTP_400_BAD_REQUEST)

#     # مسار مؤقت للصورة الأصلية
#     temp_name = f"{uuid.uuid4().hex}.jpg"
#     temp_path = os.path.join(settings.MEDIA_ROOT, "temp", temp_name)
#     os.makedirs(os.path.dirname(temp_path), exist_ok=True)

#     # حفظ الصورة الأصلية
#     with open(temp_path, 'wb+') as f:
#         for chunk in image_file.chunks():
#             f.write(chunk)

#     try:
#         # تحليل الصورة
       
#         analyzer = AdvancedDentalAnalysis(
#             detection_model_path="E:/django/dentist/project/model/best.pt",
#             classification_model_path="E:/django/dentist/project/model/tooth_model.h5"
#         )

#         results = analyzer.detect_and_classify(temp_path)
#         report = analyzer.generate_report(results)

#         # الصورة المعالجة (annotated image)
#         annotated_img = report['visualization']

#         # حفظ الصورة المعالجة
#         annotated_name = f"annotated_{uuid.uuid4().hex}.jpg"
#         annotated_path = os.path.join(
#             settings.MEDIA_ROOT, "annotated", annotated_name)
#         os.makedirs(os.path.dirname(annotated_path), exist_ok=True)
#         cv2.imwrite(annotated_path, annotated_img)

#         # حذف الصورة الأصلية بعد التحليل
#         os.remove(temp_path)

#         # بناء الرابط النسبي
#         relative_path = f"{settings.MEDIA_URL}annotated/{annotated_name}"

#         return Response({
#             'summary': report['summary'],
#             'details': report['detailed_findings'],
#             'annotated_image_path': relative_path,
#         }, status=status.HTTP_200_OK)

#     except Exception as e:
#         if os.path.exists(temp_path):
#             os.remove(temp_path)
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['POST'])
@permission_classes([IsAuthenticated])

def analyze_image99(request):
    image_file = request.FILES.get('image')
    patient_id = request.data.get('patient_id')

    if not image_file or not patient_id:
        return Response({'error': 'الرجاء إرسال صورة و patient_id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # تأكد أن المريض موجود ويتبع للطبيب الحالي
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع لهذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    # مسار مؤقت لحفظ الصورة الأصلية
    temp_name = f"{uuid.uuid4().hex}.jpg"
    temp_path = os.path.join(settings.MEDIA_ROOT, "temp", temp_name)
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)

    with open(temp_path, 'wb+') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    try:
        # تحليل الصورة
        analyzer = AdvancedDentalAnalysis(
            detection_model_path="E:/django/dentist/project/model/best.pt",
            classification_model_path="E:/django/dentist/project/model/tooth_model.h5"
        )

        results = analyzer.detect_and_classify(temp_path)
        report = analyzer.generate_report(results)
        annotated_img = report['visualization']

        # حفظ الصورة المشروحة
        annotated_name = f"annotated_{uuid.uuid4().hex}.jpg"
        annotated_path = os.path.join(settings.MEDIA_ROOT, "annotated", annotated_name)
        os.makedirs(os.path.dirname(annotated_path), exist_ok=True)
        cv2.imwrite(annotated_path, annotated_img)

        # إنشاء التقرير في قاعدة البيانات
        analysis = AnalysisReport.objects.create(
            patient=patient,
            summary=report['summary'],
            annotated_image=f"annotated/{annotated_name}"
        )

        for finding in report['detailed_findings']:
            Finding.objects.create(
                report=analysis,
                detection_class=finding['detection_class'],
                detection_confidence=finding['detection_confidence'],
                classification_class=finding['classification_class'],
                classification_confidence=finding['classification_confidence'],
                classification_details=finding['classification_details'],
                bbox=finding['bbox']
            )

        os.remove(temp_path)

        return Response({
            'summary': analysis.summary,
            'annotated_image_path': settings.MEDIA_URL + f"annotated/{annotated_name}",
            'report_id': analysis.id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([IsAuthenticated])

@permission_classes([IsAuthenticated])
def get_patient_reports(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id, doctor=request.user)
    except Patient.DoesNotExist:
        return Response({'error': 'المريض غير موجود أو لا يتبع لهذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    reports = AnalysisReport.objects.filter(patient=patient).order_by('-created_at')
    serializer = AnalysisReportSerializer(reports, many=True, context={'request': request})
    return Response(serializer.data)



###########################################

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_image(request):
    radiograph_id = request.data.get('radiograph_id')
    if not radiograph_id:
        return Response({'error': 'الرجاء إرسال radiograph_id'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # جلب صورة الأشعة والتأكد من أنها تابعة لمريض يتبع الطبيب الحالي
        radiograph = Radiograph.objects.get(id=radiograph_id, patient__doctor=request.user)
    except Radiograph.DoesNotExist:
        return Response({'error': 'صورة الأشعة غير موجودة أو المريض لا يتبع لهذا الطبيب'}, status=status.HTTP_404_NOT_FOUND)

    image_path = os.path.join(settings.MEDIA_ROOT, radiograph.photo.name)

    try:
        analyzer = AdvancedDentalAnalysis(
            detection_model_path="E:/django/dentist/project/model/best.pt",
            classification_model_path="E:/django/dentist/project/model/tooth_model.h5"
        )

        results = analyzer.detect_and_classify(image_path)
        report = analyzer.generate_report(results)
        annotated_img = report['visualization']

        # حفظ الصورة المشروحة
        annotated_name = f"annotated_{uuid.uuid4().hex}.jpg"
        annotated_path = os.path.join(settings.MEDIA_ROOT, "annotated", annotated_name)
        os.makedirs(os.path.dirname(annotated_path), exist_ok=True)
        cv2.imwrite(annotated_path, annotated_img)

        # إنشاء التقرير مع ربطه بصورة الأشعة
        analysis = AnalysisReport.objects.create(
            patient=radiograph.patient,
            radiograph=radiograph,
            summary=report['summary'],
            annotated_image=f"annotated/{annotated_name}"
        )

        for finding in report['detailed_findings']:
            Finding.objects.create(
                report=analysis,
                detection_class=finding['detection_class'],
                detection_confidence=finding['detection_confidence'],
                classification_class=finding['classification_class'],
                classification_confidence=finding['classification_confidence'],
                classification_details=finding['classification_details'],
                bbox=finding['bbox']
            )

        return Response({
            'summary': analysis.summary,
            'annotated_image_path': settings.MEDIA_URL + f"annotated/{annotated_name}",
            'report_id': analysis.id
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



