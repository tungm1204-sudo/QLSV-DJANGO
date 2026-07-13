from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from .models import Role, SystemConfig, AuditLog, Notification
from .serializers import (
    UserSerializer, 
    UserCreateUpdateSerializer, 
    CustomTokenObtainPairSerializer,
    LoginSessionSerializer,
    RoleSerializer,
    SystemConfigSerializer,
    NotificationSerializer,
    AuditLogSerializer
)
from .services import AuthService, UserService, log_audit
from .selectors import AuthSelector, NotificationSelector, AuditLogSelector

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            email = request.data.get('email')
            if email:
                user = User.objects.filter(email=email).first()
                if user:
                    AuthService.record_login(user, request)
                    log_audit(user, 'LOGIN', 'Auth', {'email': email}, request)
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
    filter_backends = [DjangoFilterBackend, SearchFilter]
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
    def login_sessions(self, request, pk=None):
        user = self.get_object()
        sessions = AuthSelector.get_login_sessions(user)
        serializer = LoginSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def import_excel(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        count, error = UserService.import_users_from_excel(file_obj, request)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
            
        log_audit(request.user, 'IMPORT_EXCEL', 'Users', {'count': count}, request)
        return Response({'message': f'Successfully imported {count} users'})

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
        return NotificationSelector.get_user_notifications(self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user', 'module']
    search_fields = ['action', 'payload']

    def get_queryset(self):
        return AuditLogSelector.get_logs()
        
    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        try:
            import openpyxl
            from openpyxl.utils import get_column_letter
        except ImportError:
            return Response({'error': 'openpyxl is not installed'}, status=status.HTTP_400_BAD_REQUEST)
            
        logs = self.filter_queryset(self.get_queryset())
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Audit Logs"
        
        headers = ["ID", "User", "Action", "Module", "IP Address", "Created At"]
        ws.append(headers)
        
        for log in logs:
            user_str = log.user.email if log.user else "System"
            ws.append([str(log.id), user_str, log.action, log.module, log.ip_address, str(log.created_at)])
            
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="audit_logs.xlsx"'
        wb.save(response)
        
        log_audit(request.user, 'EXPORT_EXCEL', 'AuditLog', None, request)
        return response

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def request_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user, code = AuthService.generate_otp(email)
    if user:
        log_audit(user, 'REQUEST_OTP', 'Auth', {'email': email}, request)
        return Response({'message': 'OTP sent successfully', 'code_for_testing': code})
    return Response({'message': 'OTP sent successfully'})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_otp(request):
    email = request.data.get('email')
    code = request.data.get('code')
    
    if not email or not code:
        return Response({'error': 'Email and code are required'}, status=status.HTTP_400_BAD_REQUEST)
        
    user, error = AuthService.verify_otp(email, code)
    if error:
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
    log_audit(user, 'VERIFY_OTP', 'Auth', {'email': email}, request)
    return Response({'message': 'OTP verified successfully'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        log_audit(request.user, 'LOGOUT', 'Auth', None, request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password(request):
    email = request.data.get('email')
    code = request.data.get('code')
    new_password = request.data.get('new_password')
    
    if not all([email, code, new_password]):
        return Response({'error': 'Email, code, and new_password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
    user, error = AuthService.verify_otp(email, code)
    if error:
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
    AuthService.reset_password(user, new_password)
    log_audit(user, 'RESET_PASSWORD', 'Auth', {'email': email}, request)
    
    return Response({'message': 'Password reset successfully'})
