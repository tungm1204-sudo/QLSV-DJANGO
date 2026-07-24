"""
Module HR Views
Lớp Controller (API endpoints). Mỏng nhất có thể.
Khởi tạo dữ liệu -> gọi Service -> Trả về Response.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.core.permissions import IsAdminOrReadOnly
from apps.core.views import get_client_ip
from .models import Student, Lecturer, Staff
from .serializers import StudentSerializer, LecturerSerializer, StaffSerializer
from .selectors import StudentSelector, LecturerSelector, StaffSelector
from .services import StudentService, LecturerService, StaffService, ImportService


class StudentViewSet(viewsets.GenericViewSet):
    """
    ViewSet quản lý Sinh viên.
    Chỉ Admin mới có quyền POST/PUT/DELETE.
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = StudentSerializer
    queryset = Student.objects.none()
    filterset_fields = ['major', 'administrative_class', 'education_system', 'status']
    search_fields = ['student_code', 'full_name', 'email', 'phone']

    def get_queryset(self):
        return StudentSelector.get_students()

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            student = StudentSelector.get_student(pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'detail': 'Sinh viên không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        student = StudentService.create_student(
            validated_data=serializer.validated_data,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            student = StudentSelector.get_student(pk)
        except Student.DoesNotExist:
            return Response({'detail': 'Sinh viên không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        updated_student = StudentService.update_student(
            student=student,
            validated_data=serializer.validated_data,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(StudentSerializer(updated_student).data)

    def destroy(self, request, pk=None):
        try:
            student = StudentSelector.get_student(pk)
        except Student.DoesNotExist:
            return Response({'detail': 'Sinh viên không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        StudentService.delete_student(
            student=student,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='import')
    def import_excel(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail': 'Vui lòng cung cấp file excel (thuộc tính: file).'}, status=status.HTTP_400_BAD_REQUEST)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        count, error = ImportService.import_students_from_excel(
            file_obj=file_obj,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if error:
            return Response({'detail': 'Lỗi import Excel', 'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': f'Import thành công {count} sinh viên.'}, status=status.HTTP_200_OK)


class LecturerViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = LecturerSerializer
    queryset = Lecturer.objects.none()
    filterset_fields = ['department', 'status']
    search_fields = ['lecturer_code', 'full_name', 'email', 'phone']

    def get_queryset(self):
        return LecturerSelector.get_lecturers()

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            lecturer = LecturerSelector.get_lecturer(pk)
            serializer = LecturerSerializer(lecturer)
            return Response(serializer.data)
        except Lecturer.DoesNotExist:
            return Response({'detail': 'Giảng viên không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = LecturerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        lecturer = LecturerService.create_lecturer(
            validated_data=serializer.validated_data,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(LecturerSerializer(lecturer).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            lecturer = LecturerSelector.get_lecturer(pk)
        except Lecturer.DoesNotExist:
            return Response({'detail': 'Giảng viên không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LecturerSerializer(lecturer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        updated_lecturer = LecturerService.update_lecturer(
            lecturer=lecturer,
            validated_data=serializer.validated_data,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(LecturerSerializer(updated_lecturer).data)

    def destroy(self, request, pk=None):
        try:
            lecturer = LecturerSelector.get_lecturer(pk)
        except Lecturer.DoesNotExist:
            return Response({'detail': 'Giảng viên không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        LecturerService.delete_lecturer(
            lecturer=lecturer,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='import')
    def import_excel(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail': 'Vui lòng cung cấp file excel (thuộc tính: file).'}, status=status.HTTP_400_BAD_REQUEST)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        count, error = ImportService.import_lecturers_from_excel(
            file_obj=file_obj,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if error:
            return Response({'detail': 'Lỗi import Excel', 'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': f'Import thành công {count} giảng viên.'}, status=status.HTTP_200_OK)


class StaffViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = StaffSerializer
    queryset = Staff.objects.none()
    filterset_fields = ['department', 'status']
    search_fields = ['staff_code', 'full_name', 'email', 'phone']

    def get_queryset(self):
        return StaffSelector.get_staffs()

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            staff = StaffSelector.get_staff(pk)
            serializer = StaffSerializer(staff)
            return Response(serializer.data)
        except Staff.DoesNotExist:
            return Response({'detail': 'Cán bộ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = StaffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        staff = StaffService.create_staff(
            validated_data=serializer.validated_data,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(StaffSerializer(staff).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            staff = StaffSelector.get_staff(pk)
        except Staff.DoesNotExist:
            return Response({'detail': 'Cán bộ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(staff, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        updated_staff = StaffService.update_staff(
            staff=staff,
            validated_data=serializer.validated_data,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(StaffSerializer(updated_staff).data)

    def destroy(self, request, pk=None):
        try:
            staff = StaffSelector.get_staff(pk)
        except Staff.DoesNotExist:
            return Response({'detail': 'Cán bộ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        StaffService.delete_staff(
            staff=staff,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='import')
    def import_excel(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'detail': 'Vui lòng cung cấp file excel (thuộc tính: file).'}, status=status.HTTP_400_BAD_REQUEST)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        count, error = ImportService.import_staffs_from_excel(
            file_obj=file_obj,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if error:
            return Response({'detail': 'Lỗi import Excel', 'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': f'Import thành công {count} nhân viên.'}, status=status.HTTP_200_OK)
