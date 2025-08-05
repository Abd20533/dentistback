from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_patients',
        verbose_name='الطبيب المعالج'
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    # conditions = models.TextField(null=True, blank=True)  # قائمة مفصولة بفواصل

    allergies = models.TextField(null=True, blank=True)
    dental_history = models.TextField(null=True, blank=True)

    image = models.ImageField(
        upload_to='profile_photos/', null=True, blank=True)

    # name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Condition(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='conditions'
    )
    name = models.CharField(max_length=100)  # مثل "السكري", "حساسية البنسلين"
    notes = models.TextField(null=True, blank=True)  # ملاحظات إضافية إن أردت
    # The `date_added` field in the `Condition` model is a `DateTimeField` that is automatically
    # populated with the current date and time when a new instance of the `Condition` model is
    # created. This is achieved by setting `auto_now_add=True` in the field definition.
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.patient.name}"


class Medication(models.Model):
    TIME_CHOICES = [
        ('morning', 'صباحاً'),
        ('noon', 'ظهراً'),
        ('evening', 'مساءً'),
        ('night', 'ليلاً'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='medications'
    )
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50, null=True, blank=True)
    times_per_day = models.PositiveIntegerField(null=True, blank=True)
    time_of_day = models.CharField(
        max_length=20,
        choices=TIME_CHOICES,
        null=True,
        blank=True
    )
    duration = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.patient.name}"


class ToothTreatment(models.Model):
    CONDITION_CHOICES = [
        ('healthy', 'سليم'),
        ('cavity', 'نخر'),
        ('filled', 'حشوة'),
        ('crowned', 'تاج'),
        ('root_canal', 'معالجة لب'),
        ('extracted', 'مقلوع'),
    ]

    TREATMENT_CHOICES = [
        ('filling', 'حشو'),
        ('extraction', 'قلع'),
        ('cleaning', 'تنظيف'),
        ('crown', 'تاج'),
        ('root_canal', 'معالجة لب'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='treatments'
    )
    image = models.CharField(max_length=200, blank=True, null=True)
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES
    )
    color = models.CharField(max_length=7, default="#FFFFFF")  # ترميز HEX
    treatment_type = models.CharField(
        max_length=20,
        choices=TREATMENT_CHOICES,
        null=True,
        blank=True
    )
    tooth_number = models.CharField(max_length=10, null=True, blank=True)
    photo = models.ImageField(upload_to='photoTooth/', null=True, blank=True)

    treatment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_treatment_type_display()} - {self.tooth_number}"


class Radiograph(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='radiographs'
    )
    photo = models.ImageField(
        upload_to='photoRadiograph/', null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"أشعة {self.patient.name} - {self.date}"
