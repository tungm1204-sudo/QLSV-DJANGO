from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.permissions import IsAdminOrReadOnly, IsAdminOrTeacherOrReadOnly
from ..models import ExamType, ExamResult
from ..serializers import ExamTypeSerializer, ExamResultSerializer, BulkExamResultSerializer

class ExamTypeViewSet(viewsets.ModelViewSet):
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer
    permission_classes = [IsAdminOrReadOnly]

class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all().select_related("student", "course", "semester", "exam_type")
    serializer_class = ExamResultSerializer
    permission_classes = [IsAdminOrTeacherOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.role == 'student':
            return qs.filter(student=user)
        if user.role == 'teacher':
            from django.db.models import Q
            return qs.filter(
                Q(course__assignments__teacher__user=user, semester__classrooms__assignments__teacher__user=user) | 
                Q(semester__classrooms__homeroom_teacher__user=user)
            ).distinct()
        return qs

    @action(detail=False, methods=["get"], url_path="grade-sheet")
    def grade_sheet(self, request):
        classroom_id = request.query_params.get("classroom")
        course_id = request.query_params.get("course")
        semester_id = request.query_params.get("semester")
        exam_type_id = request.query_params.get("exam_type")
        
        if not all([classroom_id, course_id, semester_id, exam_type_id]):
            return Response({"error": "Vui lòng cung cấp đủ classroom, course, semester, exam_type"}, status=status.HTTP_400_BAD_REQUEST)
        
        from ..models import ClassroomStudent
        enrollments = ClassroomStudent.objects.filter(classroom_id=classroom_id).select_related("student", "student__student_profile")
        
        results = ExamResult.objects.filter(
            course_id=course_id,
            semester_id=semester_id,
            exam_type_id=exam_type_id,
            student__in=[e.student for e in enrollments]
        )
        result_map = {res.student_id: res for res in results}
        
        data = []
        for enrollment in enrollments:
            student = enrollment.student
            res = result_map.get(student.id)
            student_profile = getattr(student, "student_profile", None)
            data.append({
                "student_id": student.id,
                "student_name": student.get_full_name(),
                "mssv": student_profile.mssv if student_profile else "",
                "marks": res.marks if res else "",
                "max_marks": res.max_marks if res else 10.0,
                "remarks": res.remarks if res else "",
                "is_recorded": bool(res)
            })
            
        return Response(data)

    @action(detail=False, methods=["post"], url_path="bulk-update")
    def bulk_update_grades(self, request):
        serializer = BulkExamResultSerializer(data=request.data)
        if serializer.is_valid():
            results_data = serializer.validated_data.get('results', [])
            updated_count = 0
            created_count = 0
            
            for res_data in results_data:
                student = res_data.get('student')
                course = res_data.get('course')
                semester = res_data.get('semester')
                exam_type = res_data.get('exam_type')
                marks = res_data.get('marks')
                max_marks = res_data.get('max_marks', 10.0)
                remarks = res_data.get('remarks', '')
                
                obj, created = ExamResult.objects.update_or_create(
                    student=student,
                    course=course,
                    semester=semester,
                    exam_type=exam_type,
                    defaults={'marks': marks, 'max_marks': max_marks, 'remarks': remarks}
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1
                    
            return Response({
                "message": f"Đã lưu điểm. Tạo mới {created_count}, cập nhật {updated_count}.",
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="student-gpa")
    def student_gpa(self, request):
        student_id = request.query_params.get("student_id")
        if not student_id:
            if request.user.role == "student":
                student_id = request.user.id
            else:
                return Response({"error": "Vui lòng cung cấp student_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        results = ExamResult.objects.filter(student_id=student_id).select_related('course', 'exam_type')
        
        course_scores = {}
        for r in results:
            c_id = r.course.id
            if c_id not in course_scores:
                course_scores[c_id] = {'credits': r.course.credits, 'total_weight': 0, 'weighted_score': 0}
            
            w = r.exam_type.weight
            score_10 = (r.marks / r.max_marks) * 10
            course_scores[c_id]['total_weight'] += w
            course_scores[c_id]['weighted_score'] += score_10 * w
            
        total_credits = 0
        total_gpa_score = 0
        
        course_details = []
        for c_id, data in course_scores.items():
            if data['total_weight'] > 0:
                final_score = data['weighted_score'] / data['total_weight']
                total_credits += data['credits']
                total_gpa_score += final_score * data['credits']
                course_details.append({
                    "course_id": c_id,
                    "credits": data['credits'],
                    "final_score": round(final_score, 2)
                })
                
        gpa_10 = total_gpa_score / total_credits if total_credits > 0 else 0
        gpa_4 = gpa_10 * 0.4  # Đơn giản hóa hệ 4
        
        return Response({
            "student_id": student_id,
            "total_credits": total_credits,
            "gpa_10": round(gpa_10, 2),
            "gpa_4": round(gpa_4, 2),
            "course_details": course_details
        })
