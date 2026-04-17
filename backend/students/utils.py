import openpyxl
from io import BytesIO
from django.http import HttpResponse
from .models import StudentProfile
from accounts.models import User

def export_students_to_excel(queryset):
    """Xuất danh sách sinh viên ra file Excel."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Danh sách sinh viên"

    # Header
    headers = ["MSSV", "Họ", "Tên", "Email", "Ngày sinh", "Giới tính", "Địa chỉ", "Trạng thái"]
    ws.append(headers)

    # Data
    for profile in queryset:
        ws.append([
            profile.mssv,
            profile.user.first_name,
            profile.user.last_name,
            profile.user.email,
            profile.dob.strftime('%Y-%m-%d') if profile.dob else '',
            profile.get_gender_display(),
            profile.address or '',
            "Đang học" if profile.status else "Nghỉ học"
        ])

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    
    return output

def import_students_from_excel(file_obj):
    """
    Import sinh viên từ file Excel.
    Expects headers: MSSV, Họ, Tên, Email, Ngày sinh(YYYY-MM-DD), Giới tính(male/female), Địa chỉ
    """
    wb = openpyxl.load_workbook(file_obj)
    ws = wb.active
    
    success_count = 0
    errors = []
    
    # Skip header
    rows = list(ws.rows)[1:]
    
    for row in rows:
        try:
            mssv = str(row[0].value).strip()
            first_name = str(row[1].value).strip()
            last_name = str(row[2].value).strip()
            email = str(row[3].value).strip()
            dob_val = row[4].value
            gender = str(row[5].value).strip().lower()
            address = str(row[6].value or '').strip()
            
            # Create User if not exists
            user, created = User.objects.get_or_create(
                username=mssv,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': User.Role.STUDENT
                }
            )
            
            if created:
                user.set_password("Student@123") # Default password
                user.save()
            
            # Create/Update Profile
            profile, _ = StudentProfile.objects.update_or_create(
                user=user,
                defaults={
                    'mssv': mssv,
                    'dob': dob_val,
                    'gender': gender if gender in ['male', 'female', 'other'] else 'male',
                    'address': address
                }
            )
            success_count += 1
        except Exception as e:
            errors.append(f"Lỗi tại hàng {success_count + 2}: {str(e)}")
            
    return success_count, errors
