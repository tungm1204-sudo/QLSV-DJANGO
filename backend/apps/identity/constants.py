# Cấu trúc: MODULE_ACTION
# Action: VIEW, CREATE, UPDATE, DELETE

PERMISSION_CHOICES = {
    # ---------------- ADMIN & HỆ THỐNG ----------------
    'USERS_VIEW': 'Xem danh sách Người dùng',
    'USERS_CREATE': 'Thêm Người dùng mới',
    'USERS_UPDATE': 'Chỉnh sửa Người dùng',
    'USERS_DELETE': 'Xóa/Khóa Người dùng',
    
    'ROLES_VIEW': 'Xem danh sách Vai trò',
    'ROLES_CREATE': 'Thêm Vai trò mới',
    'ROLES_UPDATE': 'Chỉnh sửa Vai trò & Phân quyền',
    'ROLES_DELETE': 'Xóa Vai trò',
    
    'SYSTEM_VIEW': 'Xem Cấu hình Hệ thống',
    'SYSTEM_UPDATE': 'Chỉnh sửa Cấu hình',
    
    'AUDIT_VIEW': 'Xem Nhật ký hệ thống',
    'AUDIT_EXPORT': 'Xuất file Nhật ký',

    # ---------------- SINH VIÊN ----------------
    'STUDENT_ENROLLMENT': 'Đăng ký học phần',
    'STUDENT_ACADEMIC_VIEW': 'Xem Thời khóa biểu & Bảng điểm',
    'STUDENT_FINANCE_VIEW': 'Xem hóa đơn & Nộp tiền học phí',
    'STUDENT_APPEAL_CREATE': 'Nộp đơn phúc khảo',

    # ---------------- GIẢNG VIÊN ----------------
    'TEACHER_CLASS_VIEW': 'Xem danh sách lớp & Điểm danh',
    'TEACHER_GRADING_UPDATE': 'Nhập điểm & Khóa điểm cuối kỳ',
    'TEACHER_APPEAL_UPDATE': 'Chấm đơn phúc khảo của sinh viên',
    'TEACHER_ADVISING': 'Công tác cố vấn học tập',

    # ---------------- GIÁO VỤ ----------------
    'MASTER_DATA_MANAGE': 'Quản lý danh mục chung',
    'CURRICULUM_MANAGE': 'Quản lý Chương trình & Mở lớp học phần',
    'EXAMS_MANAGE': 'Quản lý Khảo thí & Lịch thi',
    'AFFAIRS_GRADUATION': 'Xét duyệt Tốt nghiệp & Cấp văn bằng',

    # ---------------- KẾ TOÁN ----------------
    'FINANCE_CONFIG': 'Thiết lập mức học phí',
    'FINANCE_INVOICE_MANAGE': 'Tính công nợ, quản lý Hóa đơn & Phiếu thu',
    'FINANCE_EXEMPTION_MANAGE': 'Quản lý Miễn giảm học phí',

    # ---------------- CÔNG TÁC SINH VIÊN (CTSV) ----------------
    'AFFAIRS_DISCIPLINE_MANAGE': 'Quản lý Điểm rèn luyện',
    'AFFAIRS_REWARD_MANAGE': 'Xét Khen thưởng & Kỷ luật',
    'AFFAIRS_SCHOLARSHIP_MANAGE': 'Quản lý Học bổng',

    # ---------------- THÔNG BÁO CHUNG ----------------
    'NOTIF_VIEW': 'Xem Thông báo',
    'NOTIF_CREATE': 'Gửi Thông báo mới',
}

SYSTEM_ROLES = ['Administrator', 'Giáo vụ', 'Giảng viên', 'Sinh viên', 'Kế toán', 'Công tác SV']

def get_permission_choices_list():
    """
    Hàm tiện ích trả về mảng danh sách quyền cho Frontend
    """
    return [{'id': key, 'name': value} for key, value in PERMISSION_CHOICES.items()]
