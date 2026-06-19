from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AcademicYear(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, unique=True)  # e.g. 2025/2026
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Semester(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=50)  # Semester 1, Semester 2
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} - {self.academic_year.name}"


class Department(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Programme(TimeStampedModel):
    LEVEL_CHOICES = [
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('degree', 'Degree'),
        ('masters', 'Masters'),
        ('phd', 'PhD'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programmes')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='degree')
    duration_years = models.PositiveSmallIntegerField(default=4)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Lecturer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='lecturer_profile')
    staff_no = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)  # Kenyan format e.g. +2547XXXXXXXX
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='lecturers')
    title = models.CharField(max_length=50, default='Lecturer')  # Prof, Dr, Mr, Ms
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        return f"{self.title} {self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Course(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='courses')
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    credit_hours = models.PositiveSmallIntegerField(default=3)
    year_of_study = models.PositiveSmallIntegerField(default=1)
    semester_number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Student(TimeStampedModel):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('graduated', 'Graduated'),
        ('deferred', 'Deferred'),
        ('expelled', 'Expelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')
    registration_no = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    county = models.CharField(max_length=100, blank=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='students')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True, related_name='students')
    current_year_of_study = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    date_admitted = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)

    class Meta:
        ordering = ['-date_admitted']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.registration_no} - {self.full_name}"


class Mark(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='marks')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='marks')
    cat_score = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                     validators=[MinValueValidator(0), MaxValueValidator(30)])
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                      validators=[MinValueValidator(0), MaxValueValidator(70)])
    total_score = models.DecimalField(max_digits=5, decimal_places=2, editable=False, default=0)
    grade = models.CharField(max_length=2, editable=False, blank=True)
    remarks = models.CharField(max_length=20, editable=False, blank=True)  # Pass / Fail

    class Meta:
        unique_together = ('student', 'course', 'semester')

    def compute_grade(self):
        total = float(self.cat_score) + float(self.exam_score)
        self.total_score = total
        if total >= 70:
            self.grade, self.remarks = 'A', 'Pass'
        elif total >= 60:
            self.grade, self.remarks = 'B', 'Pass'
        elif total >= 50:
            self.grade, self.remarks = 'C', 'Pass'
        elif total >= 40:
            self.grade, self.remarks = 'D', 'Pass'
        else:
            self.grade, self.remarks = 'E', 'Fail'

    def save(self, *args, **kwargs):
        self.compute_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.registration_no} - {self.course.code}: {self.total_score}"


class FeeStructure(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='fee_structures')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='fee_structures')
    year_of_study = models.PositiveSmallIntegerField(default=1)
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # KES

    class Meta:
        unique_together = ('programme', 'academic_year', 'year_of_study')

    def __str__(self):
        return f"{self.programme.code} - Y{self.year_of_study} - KES {self.amount}"


class FeePayment(TimeStampedModel):
    METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='mpesa')
    transaction_code = models.CharField(max_length=50, blank=True)  # M-Pesa code
    payment_date = models.DateTimeField(auto_now_add=True)
    narration = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.student.registration_no} - KES {self.amount_paid} ({self.method})"