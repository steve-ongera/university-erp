from rest_framework import serializers
from django.db.models import Sum
from .models import (
    AcademicYear, Semester, Department, Programme,
    Lecturer, Course, Student, Mark, FeeStructure, FeePayment
)


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)

    class Meta:
        model = Semester
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    programme_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = '__all__'

    def get_programme_count(self, obj):
        return obj.programmes.count()


class ProgrammeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Programme
        fields = '__all__'

    def get_student_count(self, obj):
        return obj.students.count()


class LecturerSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    course_count = serializers.SerializerMethodField()

    class Meta:
        model = Lecturer
        fields = '__all__'

    def get_course_count(self, obj):
        return obj.courses.count()


class CourseSerializer(serializers.ModelSerializer):
    programme_name = serializers.CharField(source='programme.name', read_only=True)
    lecturer_name = serializers.CharField(source='lecturer.full_name', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    programme_name = serializers.CharField(source='programme.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def get_balance(self, obj):
        try:
            fee = FeeStructure.objects.get(
                programme=obj.programme,
                academic_year=obj.academic_year,
                year_of_study=obj.current_year_of_study
            )
            paid = obj.payments.filter(academic_year=obj.academic_year).aggregate(
                total=Sum('amount_paid'))['total'] or 0
            return float(fee.amount) - float(paid)
        except FeeStructure.DoesNotExist:
            return None


class MarkSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    registration_no = serializers.CharField(source='student.registration_no', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)

    class Meta:
        model = Mark
        fields = '__all__'
        read_only_fields = ('total_score', 'grade', 'remarks')


class FeeStructureSerializer(serializers.ModelSerializer):
    programme_name = serializers.CharField(source='programme.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)

    class Meta:
        model = FeeStructure
        fields = '__all__'


class FeePaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    registration_no = serializers.CharField(source='student.registration_no', read_only=True)

    class Meta:
        model = FeePayment
        fields = '__all__'


# ---------- Dashboard / Analytics ----------

class DashboardSummarySerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
    total_lecturers = serializers.IntegerField()
    total_programmes = serializers.IntegerField()
    total_departments = serializers.IntegerField()
    total_fees_collected = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_fees_expected = serializers.DecimalField(max_digits=14, decimal_places=2)
    pass_rate = serializers.FloatField()