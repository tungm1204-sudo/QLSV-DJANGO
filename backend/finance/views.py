from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TuitionFee
from .serializers import TuitionFeeSerializer

class TuitionFeeViewSet(viewsets.ModelViewSet):
    queryset = TuitionFee.objects.select_related('student', 'student__user').all()
    serializer_class = TuitionFeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'student_profile'):
            return self.queryset.filter(student=user.student_profile)
        return self.queryset

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        if hasattr(request.user, 'student_profile'):
            return Response({'detail': 'Bạn không có quyền thực hiện thao tác này.'}, status=status.HTTP_403_FORBIDDEN)
            
        fee = self.get_object()
        fee.status = 'PAID'
        fee.save()
        return Response({'status': 'Thanh toán thành công', 'id': fee.id, 'new_status': fee.status})
