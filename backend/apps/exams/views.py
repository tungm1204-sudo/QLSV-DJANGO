from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from apps.exams.models import ExamSession, ExamRoom, GradeReview, GradeHistory, StudentAcademicRecord
from apps.enrollment.models import Enrollment
from apps.exams.serializers import (
    ExamSessionSerializer, ExamRoomReadSerializer, ExamRoomWriteSerializer,
    GradeReviewReadSerializer, GradeReviewWriteSerializer, GradeReviewApproveSerializer,
    GradeHistorySerializer, StudentAcademicRecordSerializer,
    EnrollmentGradeUpdateSerializer, ImportGradesSerializer
)
from apps.exams.services import (
    update_enrollment_grades,
    lock_course_offering_grades,
    import_grades_from_excel,
    calculate_student_semester_gpa,
    calculate_student_cumulative_gpa,
    process_grade_review
)

class ExamSessionViewSet(viewsets.ModelViewSet):
    queryset = ExamSession.objects.all()
    serializer_class = ExamSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='generate-rooms/(?P<course_offering_id>[^/.]+)')
    def generate_rooms(self, request, pk=None, course_offering_id=None):
        """API để tạo phòng thi tự động cho một lớp học phần thuộc kỳ thi này."""
        session = self.get_object()
        capacity = int(request.data.get('students_per_room', 40))
        exam_date = request.data.get('exam_date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        
        if not all([exam_date, start_time, end_time]):
            return Response({'detail': 'Thiếu thời gian thi.'}, status=status.HTTP_400_BAD_REQUEST)
            
        from apps.exams.services import generate_exam_rooms
        try:
            rooms = generate_exam_rooms(
                course_offering_id=course_offering_id,
                exam_session_id=session.id,
                students_per_room=capacity,
                exam_date=exam_date,
                start_time=start_time,
                end_time=end_time
            )
            return Response({'status': f'Đã tạo {len(rooms)} phòng thi.'})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='export-schedule')
    def export_schedule(self, request, pk=None):
        """Xuất lịch thi ra file CSV"""
        import csv
        from django.http import HttpResponse
        
        session = self.get_object()
        rooms = ExamRoom.objects.filter(exam_session=session).select_related('course_offering__course', 'room', 'supervisor__user')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="lich_thi_{session.id}.csv"'
        
        # Add UTF-8 BOM for Excel compatibility
        response.write('\ufeff'.encode('utf8'))
        writer = csv.writer(response)
        writer.writerow(['Ngày thi', 'Bắt đầu', 'Kết thúc', 'Môn học', 'Phòng thi', 'Sức chứa', 'Giám thị'])
        
        for r in rooms:
            writer.writerow([
                r.exam_date, r.start_time, r.end_time,
                r.course_offering.course.name,
                r.room.code if r.room else '',
                r.capacity,
                r.supervisor.user.full_name if r.supervisor else ''
            ])
            
        return response

class ExamRoomViewSet(viewsets.ModelViewSet):
    queryset = ExamRoom.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ExamRoomWriteSerializer
        return ExamRoomReadSerializer

class GradeReviewViewSet(viewsets.ModelViewSet):
    queryset = GradeReview.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GradeReviewWriteSerializer
        return GradeReviewReadSerializer
        
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        review = self.get_object()
        serializer = GradeReviewApproveSerializer(data=request.data)
        if serializer.is_valid():
            try:
                process_grade_review(
                    grade_review=review,
                    new_score=serializer.validated_data['new_score'],
                    staff_id=serializer.validated_data['staff_id']
                )
                return Response({'status': 'Grade review approved and score updated.'})
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GradeHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GradeHistory.objects.all()
    serializer_class = GradeHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['enrollment__student_id', 'enrollment__course_offering_id']

class StudentAcademicRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentAcademicRecord.objects.all()
    serializer_class = StudentAcademicRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['student_id', 'semester_id']
    
    @action(detail=False, methods=['post'], url_path='calculate')
    def calculate(self, request):
        """Kích hoạt tính điểm cho sinh viên. Body: { 'student_id': UUID, 'semester_id': UUID }"""
        student_id = request.data.get('student_id')
        semester_id = request.data.get('semester_id')
        
        if not student_id or not semester_id:
            return Response({"detail": "Thiếu student_id hoặc semester_id."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # 1. Tính GPA kỳ
            calculate_student_semester_gpa(student_id=student_id, semester_id=semester_id)
            # 2. Cập nhật CPA
            calculate_student_cumulative_gpa(student_id=student_id)
            return Response({"status": "Calculation completed successfully."})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='process-warnings/(?P<semester_id>[^/.]+)')
    def process_warnings(self, request, semester_id=None):
        """Kích hoạt quét và gửi thông báo cảnh báo học vụ."""
        from apps.exams.services import process_academic_warnings
        try:
            count = process_academic_warnings(semester_id=semester_id)
            return Response({'status': f'Đã phát hiện và gửi {count} cảnh báo học vụ.'})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='export-transcript/(?P<student_id>[^/.]+)')
    def export_transcript(self, request, student_id=None):
        """Xuất bảng điểm (các học phần đã học) của sinh viên ra CSV."""
        import csv
        from django.http import HttpResponse
        
        enrollments = Enrollment.objects.filter(
            student_id=student_id,
            total_score__isnull=False
        ).select_related('course_offering__course', 'course_offering__semester').order_by('course_offering__semester__start_date')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="bang_diem_{student_id}.csv"'
        response.write('\ufeff'.encode('utf8'))
        
        writer = csv.writer(response)
        writer.writerow(['Học kỳ', 'Môn học', 'Số TC', 'Điểm QT', 'Điểm GK', 'Điểm CK', 'Điểm Hệ 10'])
        
        for e in enrollments:
            writer.writerow([
                e.course_offering.semester.name,
                e.course_offering.course.name,
                e.course_offering.course.credits,
                e.attendance_score,
                e.midterm_score,
                e.final_score,
                e.total_score
            ])
            
        return response

class GradingViewSet(viewsets.ViewSet):
    """ViewSet để xử lý việc nhập điểm cho Enrollment (Giảng viên/Giáo vụ gọi)"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'], url_path='update-grade/(?P<enrollment_id>[^/.]+)')
    def update_grade(self, request, enrollment_id=None):
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id)
        except Enrollment.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = EnrollmentGradeUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                enr = update_enrollment_grades(
                    enrollment=enrollment,
                    changed_by=request.user,
                    attendance=serializer.validated_data.get('attendance_score'),
                    midterm=serializer.validated_data.get('midterm_score'),
                    final=serializer.validated_data.get('final_score'),
                    reason=serializer.validated_data.get('reason', 'Cập nhật điểm')
                )
                return Response({'status': 'Grade updated', 'total_score': enr.total_score})
            except ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='lock-course/(?P<course_offering_id>[^/.]+)')
    def lock_course(self, request, course_offering_id=None):
        lock = request.data.get('lock', True)
        lock_course_offering_grades(course_offering_id=course_offering_id, locked=lock)
        return Response({'status': f'Course grades {"locked" if lock else "unlocked"}.'})

    @action(detail=False, methods=['post'], url_path='import-excel/(?P<course_offering_id>[^/.]+)', parser_classes=[])
    def import_excel(self, request, course_offering_id=None):
        # Lưu ý: Cần thêm MultiPartParser
        from rest_framework.parsers import MultiPartParser, FormParser
        self.parser_classes = (MultiPartParser, FormParser)
        
        serializer = ImportGradesSerializer(data=request.data)
        if serializer.is_valid():
            try:
                import_grades_from_excel(
                    course_offering_id=course_offering_id,
                    file_obj=serializer.validated_data['file'],
                    changed_by=request.user
                )
                return Response({'status': 'Grades imported successfully.'})
            except ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
