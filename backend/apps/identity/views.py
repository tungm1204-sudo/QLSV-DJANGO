from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import LoginHistory
from .serializers import (
    UserSerializer, 
    UserCreateUpdateSerializer, 
    CustomTokenObtainPairSerializer,
    LoginHistorySerializer
)

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Get user from email
            email = request.data.get('email')
            if email:
                try:
                    user = User.objects.get(email=email)
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])
                    
                    # Record Login History
                    ip_address = request.META.get('REMOTE_ADDR')
                    user_agent = request.META.get('HTTP_USER_AGENT')
                    LoginHistory.objects.create(
                        user=user,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        device_info="Unknown" # Can be enhanced later
                    )
                except User.DoesNotExist:
                    pass
        return response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    # For now, require auth, but not checking specific roles yet
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateUpdateSerializer
        return UserSerializer

    # Optional: custom endpoint to get login history for a specific user
    from rest_framework.decorators import action
    @action(detail=True, methods=['get'])
    def login_history(self, request, pk=None):
        user = self.get_object()
        histories = user.login_histories.all()[:50] # Get last 50
        serializer = LoginHistorySerializer(histories, many=True)
        return Response(serializer.data)
