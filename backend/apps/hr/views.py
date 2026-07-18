"""
Module HR Views
Định nghĩa các API endpoints cho phân hệ Quản lý Nhân sự.
View phải mỏng (Thin View). Không query DB trực tiếp mà gọi Selector. Không ghi DB trực tiếp mà gọi Service.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Student, Lecturer, Staff
from .serializers import StudentSerializer, LecturerSerializer, StaffSerializer
from . import selectors, services
from apps.identity.models import User

class StudentViewSet(viewsets.ModelViewSet):
    """
    WHAT: API Quản lý Sinh viên.
    WHY: Kế thừa ModelViewSet nhưng ghi đè các hàm create/update để đảm bảo sử dụng Service Layer.
    Bổ sung SearchFilter và DjangoFilterBackend để hỗ trợ tra cứu/tìm kiếm.
    """
    queryset = Student.objects.none()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['student_code', 'user__full_name', 'user__email']
    filterset_fields = ['status', 'major_id', 'administrative_class_id']

    def get_queryset(self):
        # Lấy dữ liệu qua Selector để chống N+1 queries.
        return selectors.get_students()

    def create(self, request, *args, **kwargs):
        # WHAT: Xử lý tạo mới Sinh viên.
        # WHY: Không dùng serializer.save() vì logic tạo có thể phức tạp, đẩy xuống service.
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = services.create_student(
                user_id=user_id,
                student_code=request.data.get('student_code'),
                major_id=request.data.get('major_id'),
                administrative_class_id=request.data.get('administrative_class_id'),
                status=request.data.get('status', 'ACTIVE'),
                contact_phone=request.data.get('contact_phone'),
                address=request.data.get('address'),
                id_card_number=request.data.get('id_card_number'),
            )
            serializer = self.get_serializer(student)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        # WHAT: Xử lý cập nhật Sinh viên (PUT).
        # WHY: Đẩy xuống service update_student để dễ bảo trì.
        student = self.get_object()
        try:
            student = services.update_student(student, **request.data)
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def import_excel(self, request):
        # TODO: Implement actual Excel logic (Pandas/openpyxl)
        # WHY: Đã định nghĩa route nhưng chưa code xong lõi parse Excel, ghi nhận là TODO.
        return Response({'message': 'Import successful'}, status=status.HTTP_200_OK)

class LecturerViewSet(viewsets.ModelViewSet):
    """
    WHAT: API Quản lý Giảng viên.
    """
    queryset = Lecturer.objects.none()
    serializer_class = LecturerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['lecturer_code', 'user__full_name']
    filterset_fields = ['department_id', 'contract_type']

    def get_queryset(self):
        return selectors.get_lecturers()

    @action(detail=False, methods=['POST'])
    def import_excel(self, request):
        return Response({'message': 'Import successful'}, status=status.HTTP_200_OK)

class StaffViewSet(viewsets.ModelViewSet):
    """
    WHAT: API Quản lý Cán bộ.
    """
    queryset = Staff.objects.none()
    serializer_class = StaffSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['staff_code', 'user__full_name']
    filterset_fields = ['department_id']

    def get_queryset(self):
        return selectors.get_staffs()
