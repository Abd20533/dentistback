from django.urls import path
from .views import analyze_image, get_patient_reports

urlpatterns = [
    path('analyze/', analyze_image, name='analyze-image'),
    path('reports/<int:patient_id>/',
         get_patient_reports, name="get_patient_reports"),

]
