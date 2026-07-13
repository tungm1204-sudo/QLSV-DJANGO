from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import AuditLog, OTPToken, LoginSession, SystemConfig
import random

User = get_user_model()

def log_audit(user, action_name, module, payload=None, request=None, record_id=None):
    ip_address = None
    user_agent = None
    if request:
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
        
    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action=action_name,
        module=module,
        payload=payload,
        record_id=record_id,
        ip_address=ip_address,
        user_agent=user_agent
    )

class AuthService:
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
    def verify_otp(email, code):
        try:
            user = User.objects.get(email=email)
            token = OTPToken.objects.filter(user=user, code=code, is_used=False).order_by('-created_at').first()
            
            if not token or not token.is_valid():
                return None, "Invalid or expired OTP"
                
            token.is_used = True
            token.save()
            
            # Clear lockout if successful OTP
            user.failed_login_attempts = 0
            user.locked_until = None
            user.save(update_fields=['failed_login_attempts', 'locked_until'])
            
            return user, None
        except User.DoesNotExist:
            return None, "Invalid or expired OTP"
            
    @staticmethod
    def reset_password(user, new_password):
        user.set_password(new_password)
        user.save()
        return True

    @staticmethod
    def record_login(user, request):
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
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
    def import_users_from_excel(file_obj, request):
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
                    user = User.objects.create_user(email=email, full_name=full_name, password=password)
                    created_count += 1
            return created_count, None
        except Exception as e:
            return 0, str(e)
