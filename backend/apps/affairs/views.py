from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from apps.affairs.models import (
    RewardDisciplineCategory, StudentRewardDiscipline,
    TrainingScore, Scholarship, AdvisingSession,
    HealthInsurance, Survey, SurveyQuestion, SurveyResponse, SurveyAnswer
)
from apps.affairs.serializers import (
    RewardDisciplineCategorySerializer,
    StudentRewardDisciplineReadSerializer, StudentRewardDisciplineWriteSerializer,
    TrainingScoreSerializer, ScholarshipSerializer,
    AdvisingSessionReadSerializer, AdvisingSessionWriteSerializer,
    HealthInsuranceSerializer, SurveyReadSerializer, SurveyWriteSerializer,
    SurveyQuestionSerializer, SurveyResponseSerializer
)
from apps.affairs.services import approve_reward_discipline, calculate_final_training_score

class RewardDisciplineCategoryViewSet(viewsets.ModelViewSet):
    queryset = RewardDisciplineCategory.objects.all()
    serializer_class = RewardDisciplineCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentRewardDisciplineViewSet(viewsets.ModelViewSet):
    queryset = StudentRewardDiscipline.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['student_id', 'semester_id', 'status', 'category__type']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StudentRewardDisciplineWriteSerializer
        return StudentRewardDisciplineReadSerializer
        
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        try:
            record = approve_reward_discipline(record_id=self.get_object().id, approved_by_id=request.user.id)
            return Response({'status': 'Approved', 'final_status': record.status})
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TrainingScoreViewSet(viewsets.ModelViewSet):
    queryset = TrainingScore.objects.all()
    serializer_class = TrainingScoreSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['student_id', 'semester_id']
    
    @action(detail=False, methods=['post'], url_path='calculate')
    def calculate(self, request):
        student_id = request.data.get('student_id')
        semester_id = request.data.get('semester_id')
        if not student_id or not semester_id:
            return Response({"detail": "Thiếu student_id hoặc semester_id."}, status=status.HTTP_400_BAD_REQUEST)
            
        record = calculate_final_training_score(student_id, semester_id)
        return Response({'status': 'Calculated', 'faculty_assessment': record.faculty_assessment})

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """Cố vấn học tập / Khoa duyệt điểm rèn luyện"""
        score = self.get_object()
        faculty_assessment = request.data.get('faculty_assessment')
        
        if faculty_assessment is not None:
            score.faculty_assessment = int(faculty_assessment)
            
        score.save()
        return Response({
            'status': 'Approved',
            'faculty_assessment': score.faculty_assessment
        })

class ScholarshipViewSet(viewsets.ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['student_id', 'semester_id', 'type', 'status']

class AdvisingSessionViewSet(viewsets.ModelViewSet):
    queryset = AdvisingSession.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['student_id', 'advisor_id', 'semester_id']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AdvisingSessionWriteSerializer
        return AdvisingSessionReadSerializer

class HealthInsuranceViewSet(viewsets.ModelViewSet):
    """
    CRUD Bảo hiểm y tế sinh viên.
    Hỗ trợ filter theo lớp (class_id), khóa (cohort_id), trạng thái.
    """
    queryset = HealthInsurance.objects.all().select_related(
        'student__user', 'student__administrative_class__cohort'
    )
    serializer_class = HealthInsuranceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['student_id', 'type', 'is_active']

    @action(detail=False, methods=['get'], url_path='export')
    def export(self, request):
        """
        Xuất danh sách BHYT ra file Excel (.xlsx).
        Hỗ trợ filter theo:
          - ?class_id=<uuid>   → lọc theo lớp hành chính
          - ?cohort_id=<uuid>  → lọc theo khóa tuyển sinh
          - ?is_active=true/false
        WHY: Dùng Excel thay CSV để tương thích với workflow nghiệp vụ thực tế.
        """
        import openpyxl
        from io import BytesIO
        from django.http import HttpResponse

        qs = self.filter_queryset(self.get_queryset())

        # Filter thêm theo lớp hoặc khóa
        class_id = request.query_params.get('class_id')
        cohort_id = request.query_params.get('cohort_id')
        if class_id:
            qs = qs.filter(student__administrative_class_id=class_id)
        if cohort_id:
            qs = qs.filter(student__administrative_class__cohort_id=cohort_id)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Danh sách BHYT'

        # Header
        headers = [
            'STT', 'MSSV', 'Họ và tên', 'Lớp', 'Khóa',
            'Loại BHYT', 'Mã thẻ BHYT', 'Ngày bắt đầu', 'Ngày kết thúc', 'Trạng thái'
        ]
        ws.append(headers)

        # Style header row
        from openpyxl.styles import Font, PatternFill
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill(fill_type='solid', fgColor='DDEEFF')

        for idx, ins in enumerate(qs, start=1):
            admin_class = ins.student.administrative_class
            cohort_name = admin_class.cohort.name if (admin_class and admin_class.cohort) else '—'
            class_name = admin_class.class_code if admin_class else '—'

            ws.append([
                idx,
                ins.student.student_code,
                ins.student.user.full_name,
                class_name,
                cohort_name,
                ins.get_type_display(),
                ins.insurance_code,
                ins.start_date.strftime('%d/%m/%Y') if ins.start_date else '',
                ins.end_date.strftime('%d/%m/%Y') if ins.end_date else '',
                'Còn hạn' if ins.is_active else 'Hết hạn',
            ])

        # Auto column width
        for col in ws.columns:
            max_len = max((len(str(cell.value or '')) for cell in col), default=0)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 40)

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="danh_sach_BHYT.xlsx"'
        return response

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['semester_id', 'is_active']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SurveyWriteSerializer
        return SurveyReadSerializer

    @action(detail=True, methods=['get'], url_path='export-results')
    def export_results(self, request, pk=None):
        """Xuất kết quả khảo sát ra file CSV"""
        import csv
        from django.http import HttpResponse
        
        survey = self.get_object()
        responses = SurveyResponse.objects.filter(survey=survey).select_related('student__user').prefetch_related('answers__question')
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="khao_sat_{survey.id}.csv"'
        response.write('\ufeff'.encode('utf8'))
        
        writer = csv.writer(response)
        
        # Get all questions for header
        questions = SurveyQuestion.objects.filter(survey=survey).order_by('order')
        header = ['MSSV', 'Họ tên', 'Ngày trả lời'] + [q.content for q in questions]
        writer.writerow(header)
        
        for resp in responses:
            row = [
                resp.student.student_code,
                resp.student.user.full_name,
                resp.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ]
            
            # Map answers to questions
            answers_dict = {ans.question_id: ans.text_answer for ans in resp.answers.all()}
            for q in questions:
                row.append(answers_dict.get(q.id, ''))
                
            writer.writerow(row)
            
        return response

class SurveyQuestionViewSet(viewsets.ModelViewSet):
    queryset = SurveyQuestion.objects.all()
    serializer_class = SurveyQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['survey_id', 'type']

class SurveyResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['survey_id', 'student_id']

    def create(self, request, *args, **kwargs):
        from apps.affairs.services import SurveyService
        from rest_framework import status
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Call service layer
        response_obj = SurveyService.create_survey_response(
            serializer.validated_data,
            actor_id=request.user.id,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response(
            self.get_serializer(response_obj).data,
            status=status.HTTP_201_CREATED
        )
