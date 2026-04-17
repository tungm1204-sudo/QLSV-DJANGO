import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
from accounts.models import User
from students.models import StudentProfile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return baker.make(User, username="admin", email="admin@example.com", role=User.Role.ADMIN)

@pytest.fixture
def auth_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.mark.django_db
class TestStudentAPI:
    def test_list_students(self, auth_client):
        # Tạo 3 sinh viên mẫu với dữ liệu hợp lệ
        from datetime import date
        for i in range(3):
            user = baker.make(User, username=f"student_{i}", role=User.Role.STUDENT)
            baker.make(StudentProfile, user=user, mssv=f"SV00{i}", dob=date(2000, 1, 1))
        
        url = reverse("student-list")
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Nếu có phân trang (pagination), data sẽ nằm trong res.data['results']
        # Nhưng DRF default ModelViewSet ko có pagination tự động trừ khi set PAGE_SIZE
        assert len(response.data) == 3 or "results" in response.data

    def test_create_student_success(self, auth_client):
        url = reverse("student-list")
        payload = {
            "mssv": "SVTEST01",
            "first_name": "Nguyen",
            "last_name": "Test",
            "email": "svtest01@example.com",
            "password": "strongpassword123",
            "dob": "2000-01-01",
            "gender": "male",
            "address": "123 Test Street",
            "phone": "0123456789"
        }
        
        response = auth_client.post(url, data=payload, format="json")
        
        assert response.status_code == status.HTTP_201_CREATED
        assert "mssv" in response.data
        assert response.data["mssv"] == "SVTEST01"
        
        # Verify db integration
        assert StudentProfile.objects.filter(mssv="SVTEST01").exists()
        assert User.objects.filter(username="SVTEST01").exists()

    def test_create_student_unauthorized(self, api_client):
        url = reverse("student-list")
        response = api_client.post(url, data={})
        
        # DRF permission check nên trả về 401
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_export_excel(self, auth_client):
        # Create a few students to export
        from datetime import date
        for i in range(2):
            user = baker.make(User, username=f"export_{i}", role=User.Role.STUDENT)
            baker.make(StudentProfile, user=user, mssv=f"EX00{i}", dob=date(2000, 1, 1))
        
        url = reverse("student-export-excel")
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        assert b"students.xlsx" in response["Content-Disposition"].encode()

    def test_import_excel(self, auth_client):
        # Create a mock Excel file
        import openpyxl
        from io import BytesIO
        
        wb = openpyxl.Workbook()
        ws = wb.active
        headers = ["MSSV", "Họ", "Tên", "Email", "Ngày sinh", "Giới tính", "Địa chỉ"]
        ws.append(headers)
        ws.append(["IM001", "Nguyen", "Van A", "vna@test.com", "2001-05-20", "male", "HCM City"])
        
        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)
        excel_file.name = 'import.xlsx'
        
        url = reverse("student-import-excel")
        response = auth_client.post(url, {'file': excel_file}, format='multipart')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert "success" in response.data
        assert StudentProfile.objects.filter(mssv="IM001").exists()
