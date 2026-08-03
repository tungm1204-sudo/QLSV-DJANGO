"""
Enrollment Views
================
Chứa logic điều hướng Request/Response cho Đăng ký học phần.
Phân quyền:
- Student chỉ được thao tác trên danh sách của chính mình.
- Admin/Staff thao tác được tất cả.
- Tránh bỏ business logic vào đây (đã chuyển hết sang services.py).
"""
import openpyxl
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.core.permissions import IsAdminOrStaff, IsStudent
from apps.enrollment import selectors, services
from apps.enrollment.models import Enrollment
from apps.enrollment.serializers import (
    EnrollmentReadSerializer,
    EnrollmentWriteSerializer,
    ChangeCourseOfferingSerializer,
    ApproveEnrollmentSerializer
)

class StudentEnrollmentViewSet(viewsets.ViewSet):
    """
    API dành cho Sinh viên để quản lý đăng ký học phần của cá nhân.
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def list(self, request):
        """
        Xem danh sách lớp đã đăng ký của sinh viên.
        """
        semester_id = request.query_params.get('semester_id')
        enrollments = selectors.get_student_enrollments(
            student_id=request.user.student_profile.id,
            semester_id=semester_id
        )
        serializer = EnrollmentReadSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='available-courses')
    def available_courses(self, request):
        """
        Xem danh sách lớp đang mở để đăng ký.
        """
        semester_id = request.query_params.get('semester_id')
        offerings = selectors.get_available_course_offerings(semester_id=semester_id)
        from apps.curriculum.serializers import CourseOfferingSerializer
        serializer = CourseOfferingSerializer(offerings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        """
        Đăng ký lớp học phần mới.
        """
        serializer = EnrollmentWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        bypass_prerequisite = serializer.validated_data['bypass_prerequisite']
        if bypass_prerequisite and not getattr(request.user, 'is_staff', False):
            bypass_prerequisite = False
        
        enrollment = services.enroll_student(
            student=request.user.student_profile,
            course_offering_id=serializer.validated_data['course_offering_id'],
            enrollment_type=serializer.validated_data['enrollment_type'],
            user=request.user,
            bypass_prerequisite=bypass_prerequisite
        )
        
        return Response(
            EnrollmentReadSerializer(enrollment).data, 
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['POST'])
    def change(self, request, pk=None):
        """
        Đổi lớp học phần (Gửi ID của bản ghi đăng ký cũ và ID của lớp học phần mới).
        """
        serializer = ChangeCourseOfferingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Đảm bảo sinh viên chỉ có thể đổi lớp của chính mình
        try:
            enrollment = Enrollment.objects.get(id=pk, student=request.user.student_profile)
        except Enrollment.DoesNotExist:
            return Response({"detail": "Không tìm thấy đăng ký."}, status=status.HTTP_404_NOT_FOUND)
            
        bypass_prerequisite = serializer.validated_data['bypass_prerequisite']
        if bypass_prerequisite and not getattr(request.user, 'is_staff', False):
            bypass_prerequisite = False

        new_enrollment = services.change_course_offering(
            enrollment_id=pk,
            new_course_offering_id=serializer.validated_data['new_course_offering_id'],
            user=request.user,
            bypass_prerequisite=bypass_prerequisite
        )
        
        return Response(
            EnrollmentReadSerializer(new_enrollment).data, 
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['POST'])
    def cancel(self, request, pk=None):
        """
        Hủy lớp đã đăng ký.
        """
        # Đảm bảo sinh viên chỉ có thể hủy lớp của chính mình
        try:
            enrollment = Enrollment.objects.get(id=pk, student=request.user.student_profile)
        except Enrollment.DoesNotExist:
            return Response({"detail": "Không tìm thấy đăng ký."}, status=status.HTTP_404_NOT_FOUND)
            
        services.cancel_enrollment(enrollment_id=pk, user=request.user)
        return Response({"detail": "Đã hủy đăng ký thành công."}, status=status.HTTP_200_OK)


class CourseOfferingEnrollmentViewSet(viewsets.ViewSet):
    """
    API dành cho Admin/Giáo vụ quản lý đăng ký của các lớp học phần.
    """
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    @action(detail=True, methods=['GET'])
    def students(self, request, pk=None):
        """
        Lấy danh sách sinh viên của một lớp học phần.
        """
        enrollments = selectors.get_course_offering_students(course_offering_id=pk)
        serializer = EnrollmentReadSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def lock(self, request, pk=None):
        """
        Chốt danh sách sinh viên (Đóng lớp).
        """
        offering = services.lock_enrollment_list(course_offering_id=pk, user=request.user)
        return Response({"detail": f"Đã chốt danh sách lớp {offering.course.code}."}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['GET'], url_path='pending-approvals')
    def pending_approvals(self, request):
        """
        Lấy danh sách các đăng ký chờ duyệt (Học cải thiện, học vượt).
        """
        enrollments = Enrollment.objects.filter(status=Enrollment.StatusChoices.PENDING).select_related(
            'student', 'course_offering'
        )
        serializer = EnrollmentReadSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], url_path='approve')
    def approve(self, request, pk=None):
        """
        Duyệt hoặc từ chối một đăng ký đặc biệt.
        """
        serializer = ApproveEnrollmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        enrollment = services.approve_enrollment(
            enrollment_id=pk,
            is_approved=serializer.validated_data['is_approved'],
            user=request.user
        )
        
        return Response(EnrollmentReadSerializer(enrollment).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def export(self, request, pk=None):
        """
        Xuất danh sách sinh viên của lớp ra file Excel.
        """
        enrollments = selectors.get_course_offering_students(course_offering_id=pk)
        
        # Khởi tạo workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Danh sách sinh viên"
        
        # Tạo header
        headers = ['STT', 'Mã SV', 'Họ tên', 'Lớp sinh viên', 'Trạng thái']
        ws.append(headers)
        
        # Ghi data
        for index, enr in enumerate(enrollments, start=1):
            student = enr.student
            ws.append([
                index,
                student.student_code,
                student.user.full_name,
                student.administrative_class.code if student.administrative_class else 'N/A',
                enr.get_status_display()
            ])
            
        # Trả về HTTP Response dạng file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Danh_sach_lop_{pk}.xlsx"'
        wb.save(response)
        
        return response
