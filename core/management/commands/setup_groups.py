from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Thiết lập quyền hạn cho hệ thống (Groups & Permissions)'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting permission setup...")
        
        # 1. Tạo các Nhóm người dùng (Groups)
        giao_vu_group, _ = Group.objects.get_or_create(name='Giáo vụ')
        sinh_vien_group, _ = Group.objects.get_or_create(name='Sinh viên')
        self.stdout.write(f"Groups checked/created: {giao_vu_group.name}, {sinh_vien_group.name}")

        # 2. Lấy danh sách Quyền (Permissions)
        # Lấy tất cả quyền của các app students, teachers, academics
        permissions = Permission.objects.filter(
            content_type__app_label__in=['students', 'teachers', 'academics']
        )
        
        # Gán TOÀN BỘ quyền cho nhóm Giáo vụ
        giao_vu_group.permissions.set(permissions)
        self.stdout.write(f"Assigned {permissions.count()} permissions to 'Giáo vụ'")
        
        # Sinh viên: Chỉ gán quyền XEM (view_...)
        view_permissions = Permission.objects.filter(
            content_type__app_label__in=['students', 'teachers', 'academics'],
            codename__startswith='view_'
        )
        sinh_vien_group.permissions.set(view_permissions)
        self.stdout.write(f"Assigned {view_permissions.count()} permissions to 'Sinh viên'")

        # 3. Tạo User mẫu để test
        # 3.1 User Giáo vụ
        giaovu_user, created = User.objects.get_or_create(username='giaovu')
        if created:
            giaovu_user.set_password('password123')
            giaovu_user.is_staff = True # is_staff=True để vào được trang Admin
            giaovu_user.save()
            self.stdout.write("Created user 'giaovu' with password 'password123'")
        else:
            # Reset password nếu user đã tồn tại
            giaovu_user.set_password('password123')
            giaovu_user.save()
            self.stdout.write("Updated user 'giaovu' password")
        
        # Thêm user giaovu vào nhóm Giáo vụ
        giaovu_user.groups.add(giao_vu_group)
        self.stdout.write("Added 'giaovu' to 'Giáo vụ' group")

        # 3.2 User Sinh viên (Demo)
        sinhvien_user, created = User.objects.get_or_create(username='sinhvien')
        if created:
            sinhvien_user.set_password('password123')
            sinhvien_user.save()
            self.stdout.write("Created user 'sinhvien' with password 'password123'")
        else:
            sinhvien_user.set_password('password123')
            sinhvien_user.save()
            self.stdout.write("Updated user 'sinhvien' password")

        # Thêm user sinhvien vào nhóm Sinh viên
        sinhvien_user.groups.add(sinh_vien_group)
        self.stdout.write("Added 'sinhvien' to 'Sinh viên' group")

        self.stdout.write(self.style.SUCCESS("\nSUCCESS: Groups, Permissions, and Users have been configured!"))
        self.stdout.write("- 'giaovu' (password123): Full Access (Giáo vụ)")
        self.stdout.write("- 'sinhvien' (password123): View Only (Sinh viên)")
