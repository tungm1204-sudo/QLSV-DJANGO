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
from .services import AuthService, UserService, RoleService, SystemConfigService, NotificationService, AuditLogService, log_audit
from .selectors import AuthSelector, NotificationSelector, AuditLogSelector

User = get_user_model()

def get_client_ip(request):
    return request.META.get('REMOTE_ADDR')

def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT')

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            email = request.data.get('email')
            if email:
                user = User.objects.filter(email=email).first()
                if user:
                    ip = get_client_ip(request)
                    ua = get_user_agent(request)
                    AuthService.record_login(user, ip, ua)
                    log_audit(user.id, 'LOGIN', 'Auth', {'email': email}, ip, ua)
        return response

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = RoleService.create_role(
            serializer.validated_data, 
            request.user.id, 
            get_client_ip(request), 
            get_user_agent(request)
        )
        return Response(RoleSerializer(role).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        role = RoleService.update_role(
            instance,
            serializer.validated_data, 
            request.user.id, 
            get_client_ip(request), 
            get_user_agent(request)
        )
        return Response(RoleSerializer(role).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        RoleService.delete_role(
            instance, 
            request.user.id, 
            get_client_ip(request), 
            get_user_agent(request)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.create_user(
            serializer.validated_data,
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = UserService.update_user(
            instance,
            serializer.validated_data,
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        return Response(UserSerializer(user).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        UserService.delete_user(
            instance,
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

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
            
        count, error = UserService.import_users_from_excel(
            file_obj, 
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'message': f'Successfully imported {count} users'})

class SystemConfigViewSet(viewsets.ModelViewSet):
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        config = SystemConfigService.create_config(
            serializer.validated_data,
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        return Response(SystemConfigSerializer(config).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        config = SystemConfigService.update_config(
            instance,
            serializer.validated_data,
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        return Response(SystemConfigSerializer(config).data)

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
        NotificationService.mark_as_read(notification)
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
        queryset = self.filter_queryset(self.get_queryset())
        wb, error = AuditLogService.export_to_excel(queryset)
        
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
            
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="audit_logs.xlsx"'
        wb.save(response)
        
        log_audit(request.user.id, 'EXPORT_EXCEL', 'AuditLog', None, get_client_ip(request), get_user_agent(request))
        return response

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def request_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user, code = AuthService.generate_otp(email)
    if user:
        log_audit(user.id, 'REQUEST_OTP', 'Auth', {'email': email}, get_client_ip(request), get_user_agent(request))
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
        
    log_audit(user.id, 'VERIFY_OTP', 'Auth', {'email': email}, get_client_ip(request), get_user_agent(request))
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
        
        log_audit(request.user.id, 'LOGOUT', 'Auth', None, get_client_ip(request), get_user_agent(request))
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
    log_audit(user.id, 'RESET_PASSWORD', 'Auth', {'email': email}, get_client_ip(request), get_user_agent(request))
    
    return Response({'message': 'Password reset successfully'})
