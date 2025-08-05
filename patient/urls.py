from django.urls import path
from . import views

urlpatterns = [
    path('addPatient/', views.addPatientToDoctor, name='addPatient'),
    path('getPatients/', views.list_patients_for_current_doctor, name='getPatients'),


    path('addMedicationToPatient/<int:patient_id>/', views.addMedicationToPatient,
         name='addMedicationToPatient'),
    path('addTreatmentToPatient/<int:patient_id>/',
         views.addTreatmentToPatient, name='addTreatmentToPatient'),
    path('addRadiographToPatient/<int:patient_id>/', views.addRadiographToPatient,
         name='addRadiographToPatient'),
    path('addPatientWithAllData/', views.addPatientWithAllData,
         name='addPatientWithAllData'),
    path('updatePatientPhone/<int:patient_id>/',
         views.update_patient_phone, name='update_patient_phone'),


path('addConditionToPatient/<int:patient_id>/', views.add_condition_to_patient, name='add_condition_to_patient'),

     #    path('updatePatientConditions/<int:patient_id>/', views.update_patient_conditions, name='update_patient_conditions'),




    path('patients/delete/<int:patient_id>/',
         views.delete_patient, name='delete-patient'),
    path('patients/<int:patient_id>/medications/delete/<int:medication_id>/',
         views.delete_medication_from_patient, name='delete-medication'),
    path('patients/<int:patient_id>/radiographs/<int:radiograph_id>/delete/',
         views.delete_radiograph_from_patient, name='delete_radiograph_from_patient'),


    path('pdf/<int:patient_id>/', views.generate_patient_pdf,
         name='generate_patient_pdf'),

    ###########################


    path('patients/<int:patient_id>/radiographs/<int:radiograph_id>/delete/',
         views.delete_radiograph_from_patient, name='delete_radiograph_from_patient'),

    # addRadiographToPatient
]
