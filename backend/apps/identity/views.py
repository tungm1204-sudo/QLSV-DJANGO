import random
from openpyxl import load_workbook, Workbook
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import LoginHistory, Role, SystemConfig, OTPToken, AuditLog, Notification
from .serializers import (
    UserSerializer, 
    UserCreateUpdateSerializer, 
    CustomTokenObtainPairSerializer,
    LoginHistorySerializer,
    RoleSerializer,
    SystemConfigSerializer,
    NotificationSerializer,
    AuditLogSerializer
)

User = get_user_model()

def log_audit(user, action_name, module, payload=None, request=None):
    ip_address = None
    user_agent = None
    if request:
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
        
    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action=action_name,
        module=module,
        payload=payload,
        ip_address=ip_address,
        user_agent=user_agent
    )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            email = request.data.get('email')
            if email:
                try:
                    user = User.objects.get(email=email)
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])
                    
                    ip_address = request.META.get('REMOTE_ADDR')
                    user_agent = request.META.get('HTTP_USER_AGENT')
                    LoginHistory.objects.create(
                        user=user,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        device_info="Unknown"
                    )
                    log_audit(user, 'LOGIN', 'Auth', {'email': email}, request)
                except User.DoesNotExist:
                    pass
        return response

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'CREATE', 'Roles', {'id': str(instance.id), 'name': instance.name}, self.request)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'UPDATE', 'Roles', {'id': str(instance.id), 'name': instance.name}, self.request)

    def perform_destroy(self, instance):
        log_audit(self.request.user, 'DELETE', 'Roles', {'id': str(instance.id), 'name': instance.name}, self.request)
        instance.delete()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'is_active', 'role']
    search_fields = ['email', 'full_name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateUpdateSerializer
        return UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'CREATE', 'Users', {'id': str(instance.id), 'email': instance.email}, self.request)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'UPDATE', 'Users', {'id': str(instance.id), 'email': instance.email}, self.request)

    def perform_destroy(self, instance):
        log_audit(self.request.user, 'DELETE', 'Users', {'id': str(instance.id), 'email': instance.email}, self.request)
        instance.delete()

    @action(detail=True, methods=['get'])
    def login_history(self, request, pk=None):
        user = self.get_object()
        histories = user.login_histories.all()[:50]
        serializer = LoginHistorySerializer(histories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def import_excel(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        try:
            wb = load_workbook(filename=file, read_only=True)
            ws = wb.active
            
            users_created = 0
            for row in ws.iter_rows(min_row=2, values_only=True):
                email = row[0]
                full_name = row[1]
                password = row[2]
                if email and full_name and password:
                    if not User.objects.filter(email=email).exists():
                        user = User.objects.create_user(email=email, password=password, full_name=full_name)
                        users_created += 1
            
            log_audit(request.user, 'IMPORT_EXCEL', 'Users', {'count': users_created}, request)
            return Response({'message': f'Successfully imported {users_created} users'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SystemConfigViewSet(viewsets.ModelViewSet):
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'CREATE', 'SystemConfig', {'key': instance.key}, self.request)

    def perform_update(self, serializer):
        instance = serializer.save()
        log_audit(self.request.user, 'UPDATE', 'SystemConfig', {'key': instance.key}, self.request)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read', 'type']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'module']
    search_fields = ['action', 'payload']

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Audit Logs"
        ws.append(['ID', 'User', 'Action', 'Module', 'IP Address', 'Created At'])
        
        for log in queryset:
            user_email = log.user.email if log.user else 'System/Guest'
            ws.append([str(log.id), user_email, log.action, log.module, log.ip_address, log.created_at.strftime("%Y-%m-%d %H:%M:%S")])
            
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=audit_logs.xlsx'
        wb.save(response)
        
        log_audit(request.user, 'EXPORT_EXCEL', 'AuditLogs', None, request)
        return response

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def request_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        code = str(random.randint(100000, 999999))
        
        OTPToken.objects.create(
            user=user,
            code=code,
            type=OTPToken.TypeChoices.LOGIN,
            expires_at=timezone.now() + timezone.timedelta(minutes=5)
        )
        
        # In a real app, send email or SMS here
        # send_mail('Your OTP', code, 'from@example.com', [email])
        
        log_audit(user, 'REQUEST_OTP', 'Auth', {'email': email}, request)
        
        # For testing, we return the code. REMOVE IN PROD.
        return Response({'message': 'OTP sent successfully', 'code_for_testing': code})
    except User.DoesNotExist:
        # Return success anyway to prevent email enumeration
        return Response({'message': 'OTP sent successfully'})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_otp(request):
    email = request.data.get('email')
    code = request.data.get('code')
    
    if not email or not code:
        return Response({'error': 'Email and code are required'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        user = User.objects.get(email=email)
        token = OTPToken.objects.filter(user=user, code=code, is_used=False).order_by('-created_at').first()
        
        if not token or not token.is_valid():
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
        token.is_used = True
        token.save()
        
        # Clear lockout if successful OTP
        user.failed_login_attempts = 0
        user.locked_until = None
        user.save(update_fields=['failed_login_attempts', 'locked_until'])
        
        log_audit(user, 'VERIFY_OTP', 'Auth', {'email': email}, request)
        
        return Response({'message': 'OTP verified successfully'})
    except User.DoesNotExist:
        return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password(request):
    email = request.data.get('email')
    code = request.data.get('code')
    new_password = request.data.get('new_password')
    
    if not email or not code or not new_password:
        return Response({'error': 'Email, code and new_password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        user = User.objects.get(email=email)
        # Should ideally use a separate token type for PASSWORD_RESET, 
        # but for simplicity we reuse the token logic here and assume OTP was sent as PASSWORD_RESET
        token = OTPToken.objects.filter(user=user, code=code, type=OTPToken.TypeChoices.PASSWORD_RESET, is_used=False).order_by('-created_at').first()
        
        if not token or not token.is_valid():
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(new_password)
        user.failed_login_attempts = 0
        user.locked_until = None
        user.save()
        
        token.is_used = True
        token.save()
        
        log_audit(user, 'RESET_PASSWORD', 'Auth', {'email': email}, request)
        return Response({'message': 'Password reset successfully'})
    except User.DoesNotExist:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
