from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    AcademicYearViewSet, SemesterViewSet, DepartmentViewSet,
    ProgrammeViewSet, LecturerViewSet, CourseViewSet,
    StudentViewSet, MarkViewSet, FeeStructureViewSet,
    FeePaymentViewSet, DashboardViewSet
)

router = DefaultRouter()
router.register(r'academic-years', AcademicYearViewSet, basename='academic-year')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'programmes', ProgrammeViewSet, basename='programme')
router.register(r'lecturers', LecturerViewSet, basename='lecturer')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'marks', MarkViewSet, basename='mark')
router.register(r'fee-structures', FeeStructureViewSet, basename='fee-structure')
router.register(r'fee-payments', FeePaymentViewSet, basename='fee-payment')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]