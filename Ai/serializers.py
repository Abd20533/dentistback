from rest_framework import serializers
from .models import AnalysisReport, Finding


class FindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finding
        fields = [
            'id',
            'detection_class',
            'detection_confidence',
            'classification_class',
            'classification_confidence',
            'classification_details',
            'bbox',
        ]


class AnalysisReportSerializer(serializers.ModelSerializer):
    findings = FindingSerializer(many=True, read_only=True)

    class Meta:
        model = AnalysisReport
        fields = [
            'id',
            'patient',
            'summary',
            'annotated_image',
            'radiograph',  # أضف هذا السطر

            'created_at',
            'findings'
        ]



