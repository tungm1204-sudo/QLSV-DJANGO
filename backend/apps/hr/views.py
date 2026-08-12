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
from .models import Student, Lecturer, Staff, StudentCertificate
from .serializers import StudentSerializer, LecturerSerializer, StaffSerializer, StudentCertificateSerializer
from .selectors import StudentSelector, LecturerSelector, StaffSelector, StudentCertificateSelector
from .services import StudentService, LecturerService, StaffService, ImportService, StudentCertificateService, ExportService


class StudentViewSet(viewsets.GenericViewSet):
    """
    ViewSet quản lý Sinh viên.
    Chỉ Admin mới có quyền POST/PUT/DELETE.
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = StudentSerializer
    queryset = Student.objects.none()
    filterset_fields = ['major', 'administrative_class', 'education_system', 'status']
    search_fields = ['student_code', 'user__full_name', 'user__email', 'contact_phone']

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
        return self._perform_update(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._perform_update(request, pk, partial=True)

    def _perform_update(self, request, pk=None, partial=False):
        try:
            student = StudentSelector.get_student(pk)
        except Student.DoesNotExist:
            return Response({'detail': 'Sinh viên không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student, data=request.data, partial=partial)
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

    @action(detail=True, methods=['get'], url_path='print-id-card')
    def print_id_card(self, request, pk=None):
        from django.http import HttpResponse
        try:
            student = StudentSelector.get_student(pk)
        except Student.DoesNotExist:
            return Response({'detail': 'Sinh viên không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        html_content = StudentService.generate_id_card(
            student=student,
            actor_id=str(request.user.id),
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        return HttpResponse(html_content, content_type='text/html')

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

    @action(detail=False, methods=['get'], url_path='export')
    def export_excel(self, request):
        from django.http import HttpResponse
        queryset = self.filter_queryset(self.get_queryset())
        columns = [
            ('Mã SV', lambda x: x.student_code),
            ('Họ tên', lambda x: x.user.full_name if x.user else ''),
            ('Email', lambda x: x.user.email if x.user else ''),
            ('SĐT', lambda x: x.contact_phone),
            ('Ngành', lambda x: x.major.name if x.major else ''),
            ('Lớp', lambda x: x.administrative_class.name if x.administrative_class else ''),
            ('Trạng thái', lambda x: x.status),
        ]
        excel_data = ExportService.export_queryset_to_excel(queryset, columns, "Students")
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="students.xlsx"'
        return response


class LecturerViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = LecturerSerializer
    queryset = Lecturer.objects.none()
    filterset_fields = ['department', 'status']
    search_fields = ['lecturer_code', 'user__full_name', 'user__email', 'contact_phone']

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

    @action(detail=False, methods=['get'], url_path='export')
    def export_excel(self, request):
        from django.http import HttpResponse
        queryset = self.filter_queryset(self.get_queryset())
        columns = [
            ('Mã GV', lambda x: x.lecturer_code),
            ('Họ tên', lambda x: x.user.full_name if x.user else ''),
            ('Khoa/Bộ môn', lambda x: x.department.name if x.department else ''),
            ('Email', lambda x: x.user.email if x.user else ''),
            ('Trạng thái', lambda x: x.status),
        ]
        excel_data = ExportService.export_queryset_to_excel(queryset, columns, "Lecturers")
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="lecturers.xlsx"'
        return response


class StaffViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = StaffSerializer
    queryset = Staff.objects.none()
    filterset_fields = ['department', 'status']
    search_fields = ['staff_code', 'user__full_name', 'user__email', 'contact_phone']

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

    @action(detail=False, methods=['get'], url_path='export')
    def export_excel(self, request):
        from django.http import HttpResponse
        queryset = self.filter_queryset(self.get_queryset())
        columns = [
            ('Mã Cán Bộ', lambda x: x.staff_code),
            ('Họ tên', lambda x: x.user.full_name if x.user else ''),
            ('Phòng ban', lambda x: x.department.name if x.department else ''),
            ('Email', lambda x: x.user.email if x.user else ''),
            ('Trạng thái', lambda x: x.status),
        ]
        excel_data = ExportService.export_queryset_to_excel(queryset, columns, "Staffs")
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="staffs.xlsx"'
        return response

class StudentCertificateViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = StudentCertificateSerializer
    queryset = StudentCertificate.objects.none()
    filterset_fields = ['student', 'status', 'certificate_type']
    search_fields = ['student__student_code', 'student__user__full_name', 'certificate_name']

    def get_queryset(self):
        return StudentCertificateSelector.get_certificates()

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
            certificate = StudentCertificateSelector.get_certificate(pk)
            serializer = StudentCertificateSerializer(certificate)
            return Response(serializer.data)
        except StudentCertificate.DoesNotExist:
            return Response({'detail': 'Chứng chỉ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = StudentCertificateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        certificate = StudentCertificateService.create_certificate(
            validated_data=serializer.validated_data,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(StudentCertificateSerializer(certificate).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            certificate = StudentCertificateSelector.get_certificate(pk)
        except StudentCertificate.DoesNotExist:
            return Response({'detail': 'Chứng chỉ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentCertificateSerializer(certificate, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        updated_certificate = StudentCertificateService.update_certificate(
            certificate=certificate,
            validated_data=serializer.validated_data,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(StudentCertificateSerializer(updated_certificate).data)

    def destroy(self, request, pk=None):
        try:
            certificate = StudentCertificateSelector.get_certificate(pk)
        except StudentCertificate.DoesNotExist:
            return Response({'detail': 'Chứng chỉ không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)

        actor_id = str(request.user.id)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        StudentCertificateService.delete_certificate(
            certificate=certificate,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
