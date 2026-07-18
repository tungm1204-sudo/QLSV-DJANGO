"""
Module HR Serializers
Định nghĩa quy tắc chuyển đổi dữ liệu (từ Object sang JSON và ngược lại) cho phân hệ Quản lý Nhân sự.
Nằm ở tầng giao tiếp (Presentation Layer), chỉ validate format, KHÔNG chứa logic nghiệp vụ.
"""
from rest_framework import serializers
from .models import Student, Lecturer, Staff

from apps.identity.serializers import UserSerializer
from apps.master_data.serializers import DepartmentSerializer, MajorSerializer

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    major_detail = MajorSerializer(source='major', read_only=True)
    administrative_class_code = serializers.CharField(source='administrative_class.code', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'user', 'student_code', 'major', 'major_detail',
            'administrative_class', 'administrative_class_code',
            'status', 'contact_phone', 'address', 'id_card_number',
            'parent_info', 'documents', 'created_at', 'updated_at'
        ]

class LecturerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_detail = DepartmentSerializer(source='department', read_only=True)

    class Meta:
        model = Lecturer
        fields = [
            'id', 'user', 'lecturer_code', 'department', 'department_detail',
            'academic_title', 'contract_type', 'teaching_domain',
            'created_at', 'updated_at'
        ]

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_detail = DepartmentSerializer(source='department', read_only=True)

    class Meta:
        model = Staff
        fields = [
            'id', 'user', 'staff_code', 'department', 'department_detail',
            'position', 'responsibilities',
            'created_at', 'updated_at'
        ]
