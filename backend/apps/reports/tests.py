from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.identity.models import User, Role
from apps.hr.models import Staff
from .models import CustomReportTemplate, DataExportHistory

class ReportTestCase(TestCase):
    def setUp(self):
        from apps.master_data.models import Department
        self.client = APIClient()
        self.role = Role.objects.create(name='ADMIN', description='Admin role')
        self.user = User.objects.create_user(email='admin@example.com', password='password', role=self.role)
        self.department = Department.objects.create(code='D01', name='Phòng Đào Tạo')
        self.staff = Staff.objects.create(user=self.user, staff_code='S001', department=self.department)
        self.client.force_authenticate(user=self.user)
        
    def test_dashboard_stats(self):
        url = reverse('dashboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_students', response.data)
        self.assertIn('total_revenue', response.data)
        
    def test_training_report(self):
        url = reverse('report-data', kwargs={'report_type': 'training'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.data, list))

    def test_invalid_report_type(self):
        url = reverse('report-data', kwargs={'report_type': 'invalid'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        
    def test_export_report(self):
        url = reverse('report-export-excel', kwargs={'report_type': 'training'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        
        # Check export history created
        self.assertEqual(DataExportHistory.objects.count(), 1)
        history = DataExportHistory.objects.first()
        self.assertEqual(history.export_type, 'training')

    def test_custom_report_template_crud(self):
        url = reverse('report-templates-list')
        data = {
            'name': 'Báo cáo SV Test',
            'report_type': 'STUDENT',
            'columns': ['full_name', 'student_code']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomReportTemplate.objects.count(), 1)
        
        template_id = response.data['id']
        detail_url = reverse('report-templates-detail', kwargs={'pk': template_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Báo cáo SV Test')
