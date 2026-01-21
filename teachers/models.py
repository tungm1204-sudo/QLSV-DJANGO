from django.db import models

class Teacher(models.Model):
    """
    Model đại diện cho Giáo viên (Giảng viên).
    Lưu trữ thông tin cá nhân của giáo viên.
    """
    teacher_id = models.AutoField(primary_key=True) # Khóa chính
    email = models.EmailField(unique=True)          # Email là duy nhất
    password = models.CharField(max_length=255)     # Mật khẩu
    fname = models.CharField(max_length=50)         # Tên
    lname = models.CharField(max_length=50)         # Họ
    dob = models.DateField()                        # Ngày sinh
    phone = models.CharField(max_length=15, blank=True, null=True)  # Số bàn
    mobile = models.CharField(max_length=15)        # Số di động
    status = models.BooleanField(default=True)      # Trạng thái (True: Đang dạy)
    last_login_date = models.DateField(blank=True, null=True)
    last_login_ip = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        """Trả về tên đầy đủ của giáo viên"""
        return f"{self.fname} {self.lname}"
