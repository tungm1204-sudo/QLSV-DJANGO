from django.core.management.base import BaseCommand
from apps.identity.models import Role
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Tạo các vai trò mặc định ban đầu cho hệ thống và tài khoản Admin'

    def handle(self, *args, **kwargs):
        roles = [
            {
                'name': 'Administrator',
                'description': 'Quản trị viên cấp cao, có toàn quyền hệ thống',
                'permissions': ['*']
            },
            {
                'name': 'Giáo vụ',
                'description': 'Quản lý đào tạo, danh mục, xếp lịch và xét tốt nghiệp',
                'permissions': [
                    'MASTER_DATA_MANAGE', 'CURRICULUM_MANAGE', 'EXAMS_MANAGE', 'AFFAIRS_GRADUATION',
                    'USERS_VIEW', 'USERS_CREATE', 'USERS_UPDATE', 'NOTIF_VIEW', 'NOTIF_CREATE', 'REPORTS_VIEW'
                ]
            },
            {
                'name': 'Giảng viên',
                'description': 'Giảng viên tham gia giảng dạy, nhập điểm, cố vấn',
                'permissions': [
                    'TEACHER_CLASS_VIEW', 'TEACHER_GRADING_UPDATE', 'TEACHER_APPEAL_UPDATE', 'TEACHER_ADVISING', 'NOTIF_VIEW'
                ]
            },
            {
                'name': 'Sinh viên',
                'description': 'Sinh viên đang theo học tại trường',
                'permissions': [
                    'STUDENT_ENROLLMENT', 'STUDENT_ACADEMIC_VIEW', 'STUDENT_FINANCE_VIEW', 'STUDENT_APPEAL_CREATE', 'NOTIF_VIEW'
                ]
            },
            {
                'name': 'Kế toán',
                'description': 'Quản lý công nợ, học phí, miễn giảm',
                'permissions': [
                    'FINANCE_CONFIG', 'FINANCE_INVOICE_MANAGE', 'FINANCE_EXEMPTION_MANAGE', 'NOTIF_VIEW'
                ]
            },
            {
                'name': 'Công tác SV',
                'description': 'Quản lý rèn luyện, khen thưởng, kỷ luật, học bổng',
                'permissions': [
                    'AFFAIRS_DISCIPLINE_MANAGE', 'AFFAIRS_REWARD_MANAGE', 'AFFAIRS_SCHOLARSHIP_MANAGE', 'NOTIF_VIEW'
                ]
            }
        ]

        admin_role = None
        for role_data in roles:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'permissions': role_data['permissions']
                }
            )
            if role.name == 'Administrator':
                admin_role = role

            # FORCE UPDATE permissions for system roles to ensure they are locked
            if not created:
                role.permissions = role_data['permissions']
                role.description = role_data['description']
                role.save()
                self.stdout.write(self.style.WARNING(f"Role updated (system enforced): {role.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Created role: {role.name}"))

        self.stdout.write(self.style.SUCCESS("Đã seed các vai trò mặc định thành công!"))

        # Create default admin user
        User = get_user_model()
        admin_email = 'admin@school.edu.vn'
        admin_password = 'Password123!'
        
        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                password=admin_password,
                role=admin_role,
                first_name='Admin',
                last_name='System'
            )
            self.stdout.write(self.style.SUCCESS(f"Đã tạo tài khoản Admin mặc định: {admin_email} / {admin_password}"))
        else:
            self.stdout.write(self.style.WARNING(f"Tài khoản {admin_email} đã tồn tại, bỏ qua tạo mới."))
