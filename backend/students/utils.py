import openpyxl
from io import BytesIO
from django.http import HttpResponse
from .models import StudentProfile
from accounts.models import User

def export_students_to_excel(queryset):
    """
    Chức năng: Tạo file Excel chứa danh sách sinh viên từ queryset đầu vào.
    Input: queryset - QuerySet của StudentProfile (đã được filter nếu cần).
    Output: (BytesIO) Buffer chứa file Excel sẵn sàng để trả về HTTP Response.
    Lưu ý: Caller phải gọi `.read()` trên buffer để lấy bytes ghi vào response.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Danh sách sinh viên"

    # Dòng tiêu đề cột — phải khớp với format của import để người dùng dùng file export làm template import
    headers = ["MSSV", "Họ", "Tên", "Email", "Ngày sinh", "Giới tính", "Địa chỉ", "Trạng thái"]
    ws.append(headers)

    # Ghi từng sinh viên thành một dòng
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
    output.seek(0) # Reset con trỏ về đầu để caller có thể đọc từ đầu file
    
    return output

def import_students_from_excel(file_obj):
    """
    Chức năng: Đọc file Excel và import sinh viên vào hệ thống hàng loạt.
    Input: file_obj - File object từ request.FILES.
    Output: (tuple) (success_count: int, errors: list[str])
        - success_count: Số lượng sinh viên import thành công.
        - errors: Danh sách chuỗi mô tả lỗi tại từng dòng thất bại.
    Yêu cầu format file: Header gồm MSSV, Họ, Tên, Email, Ngày sinh(YYYY-MM-DD), Giới tính(male/female), Địa chỉ.
    """
    wb = openpyxl.load_workbook(file_obj)
    ws = wb.active
    
    success_count = 0
    errors = []
    
    # Bỏ qua dòng đầu tiên (header) và lấy các dòng dữ liệu
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
            
            # Business logic: Dùng get_or_create để tránh tạo User trùng lặp.
            # Nếu sinh viên đã có tài khoản (import lần 2), chỉ cập nhật profile.
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
                # Mật khẩu mặc định khi tạo mới — sinh viên buộc phải đổi sau khi nhận tài khoản
                user.set_password("Student@123") # Default password
                user.save()
            
            # Dùng update_or_create: nếu profile đã tồn tại thì cập nhật, chưa có thì tạo mới
            profile, _ = StudentProfile.objects.update_or_create(
                user=user,
                defaults={
                    'mssv': mssv,
                    'dob': dob_val,
                    'gender': gender if gender in ['male', 'female', 'other'] else 'male', # Fallback về 'male' nếu giá trị không hợp lệ
                    'address': address
                }
            )
            success_count += 1
        except Exception as e:
            # Ghi nhận lỗi nhưng tiếp tục xử lý các dòng còn lại thay vì dừng toàn bộ
            errors.append(f"Lỗi tại hàng {success_count + 2}: {str(e)}")
            
    return success_count, errors
