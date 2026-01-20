import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qlsv.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

def setup_permissions():
    print("Starting permission setup...")
    
    # 1. Create Groups
    giao_vu_group, _ = Group.objects.get_or_create(name='Giáo vụ')
    sinh_vien_group, _ = Group.objects.get_or_create(name='Sinh viên')
    print(f"Groups checked/created: {giao_vu_group.name}, {sinh_vien_group.name}")

    # 2. Get Permissions
    # We want to give Giao vu all permissions for Students, Teachers, Academics
    permissions = Permission.objects.filter(
        content_type__app_label__in=['students', 'teachers', 'academics']
    )
    
    # Giao vu: All permissions
    giao_vu_group.permissions.set(permissions)
    print(f"Assigned {permissions.count()} permissions to 'Giáo vụ'")
    
    # Sinh vien: Only view permissions
    view_permissions = Permission.objects.filter(
        content_type__app_label__in=['students', 'teachers', 'academics'],
        codename__startswith='view_'
    )
    sinh_vien_group.permissions.set(view_permissions)
    print(f"Assigned {view_permissions.count()} permissions to 'Sinh viên'")

    # 3. Create/Update Users
    # 3.1 Giao Vu User
    giaovu_user, created = User.objects.get_or_create(username='giaovu')
    if created:
        giaovu_user.set_password('password123')
        giaovu_user.is_staff = True # Needed to access some admin-like features if used, but mainly for designation
        giaovu_user.save()
        print("Created user 'giaovu' with password 'password123'")
    else:
        # Reset password just in case
        giaovu_user.set_password('password123')
        giaovu_user.save()
        print("Updated user 'giaovu' password")
    
    # Ensure giaovu is in group
    giaovu_user.groups.add(giao_vu_group)
    print("Added 'giaovu' to 'Giáo vụ' group")

    # 3.2 Sinh Vien User (Demo)
    sinhvien_user, created = User.objects.get_or_create(username='sinhvien')
    if created:
        sinhvien_user.set_password('password123')
        sinhvien_user.save()
        print("Created user 'sinhvien' with password 'password123'")
    else:
         # Reset password just in case
        sinhvien_user.set_password('password123')
        sinhvien_user.save()
        print("Updated user 'sinhvien' password")

    # Ensure sinhvien is in group
    sinhvien_user.groups.add(sinh_vien_group)
    print("Added 'sinhvien' to 'Sinh viên' group")

    print("\nSUCCESS: Groups, Permissions, and Users have been configured!")
    print("- 'giaovu' (password123): Full Access (Giáo vụ)")
    print("- 'sinhvien' (password123): View Only (Sinh viên)")

if __name__ == "__main__":
    setup_permissions()
