from django.db import models
from patient.models import Patient  # إن أردت ربط التحليل بمريض
from django.utils import timezone
from patient.models import Patient, Radiograph  # أضف Radiograph

class AnalysisReport(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='analysis_reports'
    )
    radiograph = models.ForeignKey(  # ربط التحليل بصورة أشعة معينة
        Radiograph, on_delete=models.SET_NULL, null=True, blank=True, related_name='analysis_reports'
    )
    summary = models.TextField()
    annotated_image = models.ImageField(upload_to='annotated/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"تحليل لـ {self.patient.name if self.patient else 'غير معروف'} في {self.created_at.date()}"


class Finding(models.Model):
    report = models.ForeignKey(
        AnalysisReport, on_delete=models.CASCADE, related_name='findings'
    )
    detection_class = models.CharField(max_length=100)
    detection_confidence = models.FloatField()
    classification_class = models.CharField(max_length=100)
    classification_confidence = models.FloatField()
    bbox = models.JSONField()  # [x1, y1, x2, y2]
    classification_details = models.JSONField()

    def __str__(self):
        return f"{self.classification_class} ({self.detection_class})"



