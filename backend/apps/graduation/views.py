from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import (
    GraduationCondition, GraduationSession, GraduationCandidate,
    Diploma, DefenseCouncil, Thesis
)
from .serializers import (
    GraduationConditionSerializer, GraduationSessionSerializer, 
    GraduationCandidateSerializer, DiplomaSerializer, 
    DefenseCouncilSerializer, ThesisSerializer
)
from . import services
from apps.hr.models import Student

class GraduationConditionViewSet(viewsets.ModelViewSet):
    queryset = GraduationCondition.objects.filter(is_deleted=False)
    serializer_class = GraduationConditionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['major', 'cohort', 'is_active']

class GraduationSessionViewSet(viewsets.ModelViewSet):
    queryset = GraduationSession.objects.filter(is_deleted=False)
    serializer_class = GraduationSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['semester', 'status']

class GraduationCandidateViewSet(viewsets.ModelViewSet):
    queryset = GraduationCandidate.objects.filter(is_deleted=False)
    serializer_class = GraduationCandidateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['session', 'status']
    search_fields = ['student__student_code', 'student__user__full_name']
    
    @action(detail=False, methods=['get'])
    def my_progress(self, request):
        """
        API cho sinh viên tự xem tiến độ tốt nghiệp của mình
        """
        try:
            # Giả sử request.user liên kết với 1 Student
            student = Student.objects.get(user=request.user)
            result = services.check_graduation_conditions(student.id)
            return Response(result)
        except Student.DoesNotExist:
            return Response({'error': 'Người dùng không phải là sinh viên'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def scan_candidates(self, request):
        """
        Quét tự động toàn bộ sinh viên đủ điều kiện để đưa vào đợt xét tốt nghiệp.
        """
        session_id = request.data.get('session_id')
        if not session_id:
            return Response({'error': 'Thiếu session_id'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            session = GraduationSession.objects.get(id=session_id)
            students = Student.objects.filter(status='STUDYING')
            added = 0
            
            for student in students:
                result = services.check_graduation_conditions(student.id)
                if result['is_eligible']:
                    # Thêm vào đợt xét nếu đủ điều kiện
                    GraduationCandidate.objects.get_or_create(
                        session=session,
                        student=student,
                        defaults={
                            'total_credits': result['total_credits'],
                            'gpa': result['gpa'],
                            'status': 'PASSED'
                        }
                    )
                    added += 1
            return Response({'status': f'Đã quét và thêm {added} sinh viên đủ điều kiện vào đợt xét.'})
        except GraduationSession.DoesNotExist:
            return Response({'error': 'Không tìm thấy đợt xét tốt nghiệp'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DiplomaViewSet(viewsets.ModelViewSet):
    queryset = Diploma.objects.filter(is_deleted=False)
    serializer_class = DiplomaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'classification']
    search_fields = ['diploma_number', 'registry_number', 'student__student_code', 'student__user__full_name']

class DefenseCouncilViewSet(viewsets.ModelViewSet):
    queryset = DefenseCouncil.objects.filter(is_deleted=False)
    serializer_class = DefenseCouncilSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['semester', 'major']
    search_fields = ['name', 'president__user__full_name']

class ThesisViewSet(viewsets.ModelViewSet):
    queryset = Thesis.objects.filter(is_deleted=False)
    serializer_class = ThesisSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['semester', 'status', 'council']
    search_fields = ['title', 'student__student_code', 'student__user__full_name']
