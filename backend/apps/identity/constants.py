# Cấu trúc: MODULE_ACTION
# Action: VIEW, CREATE, UPDATE, DELETE

PERMISSION_CHOICES = {
    # Nhóm Người dùng (Users)
    'USERS_VIEW': 'Xem danh sách Người dùng',
    'USERS_CREATE': 'Thêm Người dùng mới',
    'USERS_UPDATE': 'Chỉnh sửa Người dùng',
    'USERS_DELETE': 'Xóa/Khóa Người dùng',
    
    # Nhóm Vai trò & Phân quyền (Roles)
    'ROLES_VIEW': 'Xem danh sách Vai trò',
    'ROLES_CREATE': 'Thêm Vai trò mới',
    'ROLES_UPDATE': 'Chỉnh sửa Vai trò & Phân quyền',
    'ROLES_DELETE': 'Xóa Vai trò',
    
    # Nhóm Cấu hình Hệ thống (System Configs)
    'SYSTEM_VIEW': 'Xem Cấu hình Hệ thống',
    'SYSTEM_UPDATE': 'Chỉnh sửa Cấu hình',
    
    # Nhóm Nhật ký Hệ thống (Audit Logs)
    'AUDIT_VIEW': 'Xem Nhật ký hệ thống',
    'AUDIT_EXPORT': 'Xuất file Nhật ký',
    
    # Nhóm Thông báo (Notifications)
    'NOTIF_VIEW': 'Xem Thông báo',
    'NOTIF_CREATE': 'Gửi Thông báo mới',
}

def get_permission_choices_list():
    """
    Hàm tiện ích trả về mảng danh sách quyền cho Frontend
    """
    return [{'id': key, 'name': value} for key, value in PERMISSION_CHOICES.items()]
