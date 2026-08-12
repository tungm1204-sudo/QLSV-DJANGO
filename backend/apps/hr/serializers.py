"""
Module HR Serializers
Định nghĩa quy tắc chuyển đổi dữ liệu (từ Object sang JSON và ngược lại) cho phân hệ Quản lý Nhân sự.
Nằm ở tầng giao tiếp (Presentation Layer), chỉ validate format, KHÔNG chứa logic nghiệp vụ.
"""
from rest_framework import serializers
from .models import Student, Lecturer, Staff, StudentCertificate

from apps.identity.serializers import UserSerializer
from apps.master_data.serializers import (
    DepartmentReadSerializer as DepartmentSerializer, 
    MajorReadSerializer as MajorSerializer,
    AdministrativeClassReadSerializer as AdministrativeClassSerializer,
    EducationSystemReadSerializer as EducationSystemSerializer,
    AdmissionTypeReadSerializer as AdmissionTypeSerializer,
    CohortReadSerializer as CohortSerializer,
    PriorityCategoryReadSerializer as PriorityCategorySerializer,
    EthnicityReadSerializer as EthnicitySerializer,
    ReligionReadSerializer as ReligionSerializer,
    NationalityReadSerializer as NationalitySerializer,
    DegreeReadSerializer as DegreeSerializer,
    AcademicTitleReadSerializer as AcademicTitleSerializer
)

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    major_detail = MajorSerializer(source='major', read_only=True)
    administrative_class_code = serializers.CharField(source='administrative_class.code', read_only=True)
    administrative_class_detail = AdministrativeClassSerializer(source='administrative_class', read_only=True)
    education_system_detail = EducationSystemSerializer(source='education_system', read_only=True)
    admission_type_detail = AdmissionTypeSerializer(source='admission_type', read_only=True)
    cohort_detail = CohortSerializer(source='cohort', read_only=True)
    priority_category_detail = PriorityCategorySerializer(source='priority_category', read_only=True)
    ethnicity_detail = EthnicitySerializer(source='ethnicity', read_only=True)
    religion_detail = ReligionSerializer(source='religion', read_only=True)
    nationality_detail = NationalitySerializer(source='nationality', read_only=True)

    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    full_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'student_code', 'major', 'major_detail',
            'administrative_class', 'administrative_class_code', 'administrative_class_detail',
            'education_system', 'education_system_detail', 
            'priority_category', 'priority_category_detail',
            'status', 'date_of_birth', 'gender', 'place_of_birth', 
            'ethnicity', 'ethnicity_detail', 
            'religion', 'religion_detail', 
            'nationality', 'nationality_detail',
            'personal_email', 'contact_phone', 'address', 'permanent_address', 'id_card_number', 'bank_account', 'health_insurance_number',
            'admission_type', 'admission_type_detail', 
            'cohort', 'cohort_detail', 
            'enrollment_date',
            'parent_info', 'documents', 'created_at', 'updated_at', 'email', 'password', 'full_name'
        ]

class LecturerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_detail = DepartmentSerializer(source='department', read_only=True)
    degree_detail = DegreeSerializer(source='degree', read_only=True)
    academic_title_detail = AcademicTitleSerializer(source='academic_title', read_only=True)
    ethnicity_detail = EthnicitySerializer(source='ethnicity', read_only=True)
    religion_detail = ReligionSerializer(source='religion', read_only=True)
    nationality_detail = NationalitySerializer(source='nationality', read_only=True)

    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    full_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Lecturer
        fields = [
            'id', 'user', 'lecturer_code', 'department', 'department_detail',
            'degree', 'degree_detail', 'academic_title', 'academic_title_detail', 'contract_type', 'teaching_domain', 'join_date', 'status',
            'date_of_birth', 'gender', 'id_card_number', 'place_of_birth', 
            'ethnicity', 'ethnicity_detail', 
            'religion', 'religion_detail', 
            'nationality', 'nationality_detail',
            'contact_phone', 'personal_email', 'address', 'bank_account',
            'created_at', 'updated_at', 'email', 'password', 'full_name'
        ]

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_detail = DepartmentSerializer(source='department', read_only=True)

    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    full_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Staff
        fields = [
            'id', 'user', 'staff_code', 'department', 'department_detail',
            'position', 'degree', 'responsibilities', 'join_date', 'status',
            'date_of_birth', 'gender', 'id_card_number', 'place_of_birth', 'ethnicity', 'religion', 'nationality',
            'contact_phone', 'personal_email', 'address', 'bank_account',
            'created_at', 'updated_at', 'email', 'password', 'full_name'
        ]

class StudentCertificateSerializer(serializers.ModelSerializer):
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    
    class Meta:
        model = StudentCertificate
        fields = '__all__'

