from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
from .models import AuditLog, OTPToken, LoginSession, SystemConfig, Role, Notification
import random

User = get_user_model()


def log_audit(user_id, action_name, module, payload=None, ip_address=None, user_agent=None, record_id=None):
    AuditLog.objects.create(
        user_id=user_id,
        action=action_name,
        module=module,
        payload=payload,
        record_id=record_id,
        ip_address=ip_address,
        user_agent=user_agent
    )


class RoleService:
    @staticmethod
    def create_role(validated_data, actor_id, ip_address=None, user_agent=None):
        role = Role.objects.create(**validated_data)
        log_audit(actor_id, 'CREATE', 'Roles', {'id': str(role.id), 'name': role.name}, ip_address, user_agent)
        return role

    @staticmethod
    def update_role(role, validated_data, actor_id, ip_address=None, user_agent=None):
        for key, value in validated_data.items():
            setattr(role, key, value)
        role.save()
        log_audit(actor_id, 'UPDATE', 'Roles', {'id': str(role.id), 'name': role.name}, ip_address, user_agent)
        return role

    @staticmethod
    def delete_role(role, actor_id, ip_address=None, user_agent=None):
        role_info = {'id': str(role.id), 'name': role.name}
        role.delete()
        log_audit(actor_id, 'DELETE', 'Roles', role_info, ip_address, user_agent)


class SystemConfigService:
    @staticmethod
    def create_config(validated_data, actor_id, ip_address=None, user_agent=None):
        config = SystemConfig.objects.create(**validated_data)
        log_audit(actor_id, 'CREATE', 'SystemConfig', {'key': config.key}, ip_address, user_agent)
        return config

    @staticmethod
    def update_config(config, validated_data, actor_id, ip_address=None, user_agent=None):
        for key, value in validated_data.items():
            setattr(config, key, value)
        config.save()
        log_audit(actor_id, 'UPDATE', 'SystemConfig', {'key': config.key}, ip_address, user_agent)
        return config


class NotificationService:
    @staticmethod
    def mark_as_read(notification):
        notification.is_read = True
        notification.save(update_fields=['is_read'])


class AuthService:
    @staticmethod
    def check_lockout(email):
        try:
            user = User.objects.get(email=email)
            if user.locked_until and user.locked_until > timezone.now():
                return True, f"Account is locked until {user.locked_until.strftime('%Y-%m-%d %H:%M:%S')} UTC."
            return False, None
        except User.DoesNotExist:
            return False, None

    @staticmethod
    def clear_lockout(user):
        user.failed_login_attempts = 0
        user.locked_until = None
        user.save(update_fields=['failed_login_attempts', 'locked_until'])

    @staticmethod
    def generate_otp(email, otp_type=OTPToken.TypeChoices.LOGIN):
        try:
            user = User.objects.get(email=email)
            code = str(random.randint(100000, 999999))
            OTPToken.objects.create(
                user=user,
                code=code,
                type=otp_type,
                expires_at=timezone.now() + timezone.timedelta(minutes=5)
            )
            return user, code
        except User.DoesNotExist:
            return None, None

    @staticmethod
    @transaction.atomic
    def verify_otp(email, code, otp_type=OTPToken.TypeChoices.LOGIN):
        """
        Fix #10: Lọc theo otp_type để OTP đăng nhập không dùng được cho reset password.
        """
        try:
            user = User.objects.get(email=email)
            token = OTPToken.objects.select_for_update().filter(
                user=user, code=code, type=otp_type, is_used=False
            ).order_by('-created_at').first()

            if not token or not token.is_valid():
                return None, "Invalid or expired OTP"

            token.is_used = True
            token.save(update_fields=['is_used'])

            user.failed_login_attempts = 0
            user.locked_until = None
            user.save(update_fields=['failed_login_attempts', 'locked_until'])

            return user, None
        except User.DoesNotExist:
            return None, "Invalid or expired OTP"

    @staticmethod
    @transaction.atomic
    def reset_password(user, new_password):
        user.set_password(new_password)
        user.save()
        return True

    @staticmethod
    @transaction.atomic
    def record_login(user, ip_address=None, user_agent=None):
        """
        Fix #5: Bọc trong @transaction.atomic — ghi user.last_login và tạo LoginSession là 1 đơn vị.
        """
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        LoginSession.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            device_info="Unknown",
            is_active=True
        )

    @staticmethod
    def handle_failed_login(email):
        try:
            user = User.objects.get(email=email)
            user.failed_login_attempts += 1

            max_attempts = 5
            try:
                config = SystemConfig.objects.get(key='MAX_LOGIN_ATTEMPTS')
                max_attempts = int(config.value)
            except (SystemConfig.DoesNotExist, ValueError):
                pass

            if user.failed_login_attempts >= max_attempts:
                user.locked_until = timezone.now() + timezone.timedelta(minutes=15)
            user.save(update_fields=['failed_login_attempts', 'locked_until'])
        except User.DoesNotExist:
            pass


class UserService:
    @staticmethod
    @transaction.atomic
    def create_user(validated_data, actor_id, ip_address=None, user_agent=None):
        """
        Fix #6: Bọc trong @transaction.atomic — tạo user và set_password là 1 đơn vị nguyên tử.
        Fix #14: Validate password bằng Django validators.
        """
        password = validated_data.pop('password', None)

        # Validate password strength trước khi tạo user
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                raise ValidationError({'password': list(e.messages)})

        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()

        log_audit(actor_id, 'CREATE', 'Users', {'id': str(user.id), 'email': user.email}, ip_address, user_agent)
        return user

    @staticmethod
    def update_user(user, validated_data, actor_id, ip_address=None, user_agent=None):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(user, key, value)
        if password:
            try:
                validate_password(password, user=user)
            except ValidationError as e:
                raise ValidationError({'password': list(e.messages)})
            user.set_password(password)
        user.save()
        log_audit(actor_id, 'UPDATE', 'Users', {'id': str(user.id), 'email': user.email}, ip_address, user_agent)
        return user

    @staticmethod
    def delete_user(user, actor_id, ip_address=None, user_agent=None):
        user_info = {'id': str(user.id), 'email': user.email}
        user.delete()
        log_audit(actor_id, 'DELETE', 'Users', user_info, ip_address, user_agent)

    @staticmethod
    @transaction.atomic
    def import_users_from_excel(file_obj, actor_id, ip_address=None, user_agent=None):
        try:
            import openpyxl
        except ImportError:
            return 0, "openpyxl is not installed"

        try:
            wb = openpyxl.load_workbook(file_obj)
            sheet = wb.active
            created_count = 0
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if not row or not row[0]:
                    continue
                email, full_name, password = row[0], row[1], row[2]
                if not User.objects.filter(email=email).exists():
                    User.objects.create_user(email=email, full_name=full_name, password=password)
                    created_count += 1

            if created_count > 0:
                log_audit(actor_id, 'IMPORT_EXCEL', 'Users', {'count': created_count}, ip_address, user_agent)
            return created_count, None
        except Exception as e:
            return 0, str(e)


class AuditLogService:
    @staticmethod
    def export_to_excel(queryset):
        try:
            import openpyxl
        except ImportError:
            return None, "openpyxl is not installed"

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Audit Logs"

        headers = ["ID", "User", "Action", "Module", "IP Address", "Created At"]
        ws.append(headers)

        for log in queryset:
            user_str = log.user.email if log.user else "System"
            ws.append([str(log.id), user_str, log.action, log.module, log.ip_address, str(log.created_at)])

        return wb, None
