from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Role, AuditLog

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
        
        # Check that audit log is created
        audit_logs = AuditLog.objects.filter(user=self.user, action='LOGIN')
        self.assertTrue(audit_logs.exists())

    def test_user_login_failure_and_lockout(self):
        url = reverse('token_obtain_pair')
        for i in range(5):
            response = self.client.post(url, {'email': 'test@example.com', 'password': 'WrongPassword'})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.locked_until)
        
        # 6th attempt should return 400 Validation Error because of lockout
        response = self.client.post(url, {'email': 'test@example.com', 'password': 'Password123!'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # In DRF, exceptions wrapped by ValidationError look like this:
        # {'detail': 'Account is locked until ...', 'code': 'account_locked'}
        # But if it's raised as ValidationError, it might be nested under `non_field_errors`.
        # Let's just assert that 'account_locked' string is somewhere in the response.
        self.assertTrue('account_locked' in str(response.data))

    def test_request_otp(self):
        url = reverse('request_otp')
        response = self.client.post(url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('code_for_testing', response.data)
        
        code = response.data['code_for_testing']
        
        verify_url = reverse('verify_otp')
        verify_response = self.client.post(verify_url, {'email': 'test@example.com', 'code': code})
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)

    def test_reset_password(self):
        url = reverse('request_otp')
        response = self.client.post(url, {'email': 'test@example.com'})
        code = response.data['code_for_testing']
        
        reset_url = reverse('reset_password')
        reset_response = self.client.post(reset_url, {
            'email': 'test@example.com',
            'code': code,
            'new_password': 'NewPassword123!'
        })
        self.assertEqual(reset_response.status_code, status.HTTP_200_OK)
        
        # Verify new password works
        login_url = reverse('token_obtain_pair')
        login_response = self.client.post(login_url, {'email': 'test@example.com', 'password': 'NewPassword123!'})
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
