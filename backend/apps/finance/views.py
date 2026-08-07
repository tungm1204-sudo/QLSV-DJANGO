"""
apps/finance/views.py
----------------------
Thin View layer cho module Tài chính.
Tuân thủ kiến trúc: View chỉ nhận Request → gọi Service → trả Response.
Tuyệt đối không viết business logic (ghi DB, tính toán) trực tiếp ở đây.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from datetime import datetime

from apps.finance.models import TuitionRule, TuitionExemption, TuitionExtension, StudentDebt, Receipt
from apps.finance.serializers import (
    TuitionRuleSerializer, TuitionExemptionSerializer,
    TuitionExtensionSerializer, StudentDebtSerializer, ReceiptSerializer
)
from apps.finance import services


class TuitionRuleViewSet(viewsets.ModelViewSet):
    """CRUD quy tắc học phí (đơn giá theo ngành/năm học)."""
    queryset = TuitionRule.objects.all()
    serializer_class = TuitionRuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class TuitionExemptionViewSet(viewsets.ModelViewSet):
    """
    CRUD hồ sơ miễn giảm học phí.
    Approve/Reject gọi Service để đảm bảo validation trạng thái và ghi log.
    """
    queryset = TuitionExemption.objects.all()
    serializer_class = TuitionExemptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Phê duyệt hồ sơ miễn giảm — gọi Service."""
        try:
            exemption = services.approve_tuition_exemption(
                exemption_id=pk,
                actor_id=str(request.user.id)
            )
            return Response(TuitionExemptionSerializer(exemption).data)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Từ chối hồ sơ miễn giảm — gọi Service."""
        try:
            exemption = services.reject_tuition_exemption(
                exemption_id=pk,
                actor_id=str(request.user.id)
            )
            return Response(TuitionExemptionSerializer(exemption).data)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TuitionExtensionViewSet(viewsets.ModelViewSet):
    """
    CRUD yêu cầu gia hạn đóng học phí.
    Approve gọi Service, Service sẽ cập nhật cả StudentDebt.due_date trong cùng transaction.
    """
    queryset = TuitionExtension.objects.all()
    serializer_class = TuitionExtensionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Phê duyệt gia hạn — gọi Service."""
        staff = getattr(request.user, 'staff', None)
        try:
            ext = services.approve_tuition_extension(
                extension_id=pk,
                approved_by_staff=staff
            )
            return Response(TuitionExtensionSerializer(ext).data)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentDebtViewSet(viewsets.ModelViewSet):
    """
    CRUD công nợ học phí sinh viên.
    Hỗ trợ filter theo lớp, học kỳ, trạng thái; tìm kiếm theo mã SV/tên.
    """
    queryset = StudentDebt.objects.filter(is_deleted=False).select_related(
        'student__user', 'student__administrative_class', 'semester'
    )
    serializer_class = StudentDebtSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student__administrative_class', 'semester', 'status']
    search_fields = ['student__student_code', 'student__user__full_name']
    ordering_fields = ['created_at', 'due_date']

    @action(detail=False, methods=['post'])
    def generate_debt(self, request):
        """Tính và sinh công nợ học phí cho 1 sinh viên trong 1 học kỳ."""
        student_id = request.data.get('student_id')
        semester_id = request.data.get('semester_id')
        due_date_str = request.data.get('due_date')

        if not student_id or not semester_id or not due_date_str:
            return Response(
                {'error': 'Thiếu tham số bắt buộc: student_id, semester_id, due_date'},
                status=status.HTTP_400_BAD_REQUEST
            )

        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

        try:
            debt = services.calculate_student_debt(student_id, semester_id, due_date)
            if not debt:
                return Response({'status': 'Sinh viên chưa đăng ký tín chỉ nào'})
            return Response(StudentDebtSerializer(debt).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def process_overdue(self, request):
        """Job trigger: cập nhật công nợ quá hạn và gửi nhắc nhở."""
        count = services.send_overdue_reminders()
        return Response({'status': f'Đã cập nhật {count} công nợ thành quá hạn'})


class ReceiptViewSet(viewsets.ModelViewSet):
    """
    CRUD phiếu thu học phí.
    Bổ sung action `print` để in/xuất HTML biên lai.
    """
    queryset = Receipt.objects.filter(is_deleted=False).select_related(
        'student__user', 'semester', 'processed_by__user'
    )
    serializer_class = ReceiptSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student__administrative_class', 'semester', 'payment_method', 'status']
    search_fields = ['student__student_code', 'student__user__full_name', 'reference_code']
    ordering_fields = ['payment_date', 'amount']

    @action(detail=True, methods=['get'], url_path='print')
    def print_receipt(self, request, pk=None):
        """
        Xuất biên lai thu học phí dạng HTML để in.
        Frontend có thể mở trong tab mới và dùng window.print() hoặc convert PDF.
        """
        try:
            html_content = services.build_receipt_html(receipt_id=pk)
            return HttpResponse(html_content, content_type='text/html; charset=utf-8')
        except Receipt.DoesNotExist:
            return Response({'detail': 'Biên lai không tồn tại.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='pay-online-callback')
    def pay_online_callback(self, request):
        """
        Stub Webhook callback từ cổng thanh toán (VNPay/Momo).
        Hiện tại là mock — sẽ tích hợp thật khi có tài khoản merchant.
        """
        debt_id = request.data.get('debt_id')
        amount = request.data.get('amount')
        reference_code = request.data.get('reference_code')

        if not debt_id or not amount:
            return Response(
                {'error': 'Thiếu tham số debt_id hoặc amount'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            receipt = services.process_payment(
                debt_id=debt_id,
                amount=float(amount),
                method='ONLINE',
                reference_code=reference_code
            )
            return Response(ReceiptSerializer(receipt).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
