from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from accounts.permissions import IsAdminOrTeacherOrReadOnly
from ..models import Attendance
from ..serializers import AttendanceSerializer, BulkAttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().select_related("student", "classroom")
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTeacherOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["date", "student", "classroom", "status"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.role == 'student':
            return qs.filter(student=user)
        if user.role == 'teacher':
            from django.db.models import Q
            return qs.filter(Q(classroom__homeroom_teacher__user=user) | Q(classroom__assignments__teacher__user=user)).distinct()
        return qs

    @action(detail=False, methods=["post"], url_path="bulk-update")
    def bulk_update_attendance(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            attendances_data = serializer.validated_data.get('attendances', [])
            updated_count = 0
            created_count = 0
            
            for att_data in attendances_data:
                student = att_data.get('student')
                classroom = att_data.get('classroom')
                date = att_data.get('date')
                status_val = att_data.get('status')
                remark = att_data.get('remark', '')
                
                obj, created = Attendance.objects.update_or_create(
                    student=student,
                    classroom=classroom,
                    date=date,
                    defaults={'status': status_val, 'remark': remark}
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1
                    
            return Response({
                "message": f"Đã lưu điểm danh. Tạo mới {created_count}, cập nhật {updated_count}.",
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
