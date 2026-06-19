from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone

from .models import (
    AcademicYear, Semester, Department, Programme,
    Lecturer, Course, Student, Mark, FeeStructure, FeePayment
)
from .serializers import (
    AcademicYearSerializer, SemesterSerializer, DepartmentSerializer,
    ProgrammeSerializer, LecturerSerializer, CourseSerializer,
    StudentSerializer, MarkSerializer, FeeStructureSerializer,
    FeePaymentSerializer
)


class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.select_related('academic_year').all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['academic_year', 'is_current']


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']


class ProgrammeViewSet(viewsets.ModelViewSet):
    queryset = Programme.objects.select_related('department').all()
    serializer_class = ProgrammeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'level', 'is_active']
    search_fields = ['name', 'code']


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.select_related('department').all()
    serializer_class = LecturerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'is_active']
    search_fields = ['first_name', 'last_name', 'staff_no', 'email']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('programme', 'lecturer').all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['programme', 'lecturer', 'year_of_study', 'semester_number']
    search_fields = ['name', 'code']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('programme', 'academic_year').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['programme', 'academic_year', 'status', 'current_year_of_study', 'gender']
    search_fields = ['first_name', 'last_name', 'registration_no', 'email']


class MarkViewSet(viewsets.ModelViewSet):
    queryset = Mark.objects.select_related('student', 'course', 'semester').all()
    serializer_class = MarkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student', 'course', 'semester', 'grade']
    search_fields = ['student__registration_no', 'course__code']

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Accepts a list of mark entries for a course/semester."""
        data = request.data
        if not isinstance(data, list):
            return Response({'error': 'Expected a list of marks'}, status=status.HTTP_400_BAD_REQUEST)
        results = []
        for entry in data:
            student_id = entry.get('student')
            course_id = entry.get('course')
            semester_id = entry.get('semester')
            mark, _ = Mark.objects.update_or_create(
                student_id=student_id, course_id=course_id, semester_id=semester_id,
                defaults={
                    'cat_score': entry.get('cat_score', 0),
                    'exam_score': entry.get('exam_score', 0),
                }
            )
            results.append(MarkSerializer(mark).data)
        return Response(results, status=status.HTTP_201_CREATED)


class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.select_related('programme', 'academic_year').all()
    serializer_class = FeeStructureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['programme', 'academic_year', 'year_of_study']


class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.select_related('student', 'academic_year').all()
    serializer_class = FeePaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student', 'academic_year', 'method']
    search_fields = ['student__registration_no', 'transaction_code']


# ---------- Dashboard Analytics Views ----------

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        total_students = Student.objects.count()
        total_lecturers = Lecturer.objects.filter(is_active=True).count()
        total_programmes = Programme.objects.filter(is_active=True).count()
        total_departments = Department.objects.count()

        fees_collected = FeePayment.objects.aggregate(total=Sum('amount_paid'))['total'] or 0
        fees_expected = FeeStructure.objects.aggregate(total=Sum('amount'))['total'] or 0

        total_marks = Mark.objects.count()
        pass_count = Mark.objects.filter(remarks='Pass').count()
        pass_rate = round((pass_count / total_marks) * 100, 2) if total_marks else 0

        return Response({
            'total_students': total_students,
            'total_lecturers': total_lecturers,
            'total_programmes': total_programmes,
            'total_departments': total_departments,
            'total_fees_collected': fees_collected,
            'total_fees_expected': fees_expected,
            'pass_rate': pass_rate,
        })

    @action(detail=False, methods=['get'])
    def enrollment_trend(self, request):
        """Students enrolled per academic year."""
        data = (
            Student.objects.values('academic_year__name')
            .annotate(count=Count('id'))
            .order_by('academic_year__name')
        )
        return Response([
            {'year': d['academic_year__name'] or 'N/A', 'students': d['count']} for d in data
        ])

    @action(detail=False, methods=['get'])
    def students_per_programme(self, request):
        data = (
            Programme.objects.annotate(student_count=Count('students'))
            .values('name', 'student_count')
            .order_by('-student_count')
        )
        return Response([
            {'programme': d['name'], 'students': d['student_count']} for d in data
        ])

    @action(detail=False, methods=['get'])
    def fees_by_year(self, request):
        data = (
            FeePayment.objects.values('academic_year__name')
            .annotate(total=Sum('amount_paid'))
            .order_by('academic_year__name')
        )
        return Response([
            {'year': d['academic_year__name'] or 'N/A', 'collected': d['total'] or 0} for d in data
        ])

    @action(detail=False, methods=['get'])
    def grade_distribution(self, request):
        data = (
            Mark.objects.values('grade')
            .annotate(count=Count('id'))
            .order_by('grade')
        )
        return Response([{'grade': d['grade'], 'count': d['count']} for d in data])

    @action(detail=False, methods=['get'])
    def gender_distribution(self, request):
        data = (
            Student.objects.values('gender')
            .annotate(count=Count('id'))
        )
        return Response([{'gender': d['gender'], 'count': d['count']} for d in data])