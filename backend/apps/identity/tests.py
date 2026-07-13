from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Role, AuditLog, OTPToken
from django.utils import timezone

User = get_user_model()


class IdentityModuleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.role = Role.objects.create(name='Student', permissions=[])
        self.user = User.objects.create_user(
            email='test@example.com',
            password='Password123!',
            full_name='Test User',
            role=self.role
        )

    def test_user_login_success(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': 'test@example.com', 'password': 'Password123!'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

        # Kiểm tra audit log được tạo sau khi login
        audit_logs = AuditLog.objects.filter(user=self.user, action='LOGIN')
        self.assertTrue(audit_logs.exists())

    def test_user_login_failure_and_lockout(self):
        """
        Test lockout: Sau 5 lần sai → tài khoản bị khoá.
        Lần tiếp theo nhận 403 Forbidden (account_locked).
        """
        url = reverse('token_obtain_pair')
        for i in range(5):
            response = self.client.post(url, {'email': 'test@example.com', 'password': 'WrongPassword'})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.locked_until)

        # Lần 6: tài khoản đã bị khoá, trả về 403 Forbidden
        response = self.client.post(url, {'email': 'test@example.com', 'password': 'Password123!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('account_locked', str(response.data))

    @override_settings(DEBUG=True)
    def test_request_otp(self):
        """
        Test OTP request và verify (type=LOGIN).
        Dùng @override_settings(DEBUG=True) để nhận code_for_testing trong test.
        """
        url = reverse('request_otp')
        response = self.client.post(url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Với DEBUG=True, code_for_testing được trả về
        self.assertIn('code_for_testing', response.data)

        code = response.data['code_for_testing']

        verify_url = reverse('verify_otp')
        verify_response = self.client.post(verify_url, {'email': 'test@example.com', 'code': code})
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)

    @override_settings(DEBUG=True)
    def test_reset_password(self):
        """
        Test reset password: Tạo OTP với type=PASSWORD_RESET, dùng để đổi mật khẩu.
        """
        # Tạo OTP type=PASSWORD_RESET trực tiếp qua DB vì request_otp endpoint tạo type=LOGIN
        from .services import AuthService
        from .models import OTPToken
        user = User.objects.get(email='test@example.com')
        code = '654321'
        OTPToken.objects.create(
            user=user,
            code=code,
            type=OTPToken.TypeChoices.PASSWORD_RESET,
            expires_at=timezone.now() + timezone.timedelta(minutes=5)
        )

        reset_url = reverse('reset_password')
        reset_response = self.client.post(reset_url, {
            'email': 'test@example.com',
            'code': code,
            'new_password': 'NewPassword123!'
        })
        self.assertEqual(reset_response.status_code, status.HTTP_200_OK)

        # Xác nhận mật khẩu mới dùng được
        login_url = reverse('token_obtain_pair')
        login_response = self.client.post(login_url, {'email': 'test@example.com', 'password': 'NewPassword123!'})
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
