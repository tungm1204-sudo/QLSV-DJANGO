from django.db import models

class Parent(models.Model):
    """
    Model đại diện cho Phụ huynh.
    Lưu trữ thông tin chi tiết về cha mẹ/người giám护 của sinh viên.
    """
    parent_id = models.AutoField(primary_key=True)  # Khóa chính tự động tăng
    fname = models.CharField(max_length=50)         # Tên
    lname = models.CharField(max_length=50)         # Họ
    dob = models.DateField()                        # Ngày sinh
    phone = models.CharField(max_length=15, blank=True, null=True)  # Số điện thoại bàn (có thể để trống)
    mobile = models.CharField(max_length=15)        # Số di động (bắt buộc)
    status = models.BooleanField(default=True)      # Trạng thái hoạt động (True: Đang hoạt động)
    last_login_date = models.DateField(blank=True, null=True)        # Ngày đăng nhập cuối
    last_login_ip = models.CharField(max_length=45, blank=True, null=True) # IP đăng nhập cuối

    def __str__(self):
        """Trả về tên đầy đủ của phụ huynh khi hiển thị object"""
        return f"{self.fname} {self.lname}"

class Student(models.Model):
    """
    Model đại diện cho Sinh viên.
    Lưu trữ thông tin cá nhân và liên kết với phụ huynh.
    """
    student_id = models.AutoField(primary_key=True) # Khóa chính tự động tăng
    email = models.EmailField(unique=True)          # Email là duy nhất
    password = models.CharField(max_length=255)     # Mật khẩu (lưu hash)
    fname = models.CharField(max_length=50)         # Tên
    lname = models.CharField(max_length=50)         # Họ
    dob = models.DateField()                        # Ngày sinh
    phone = models.CharField(max_length=15, blank=True, null=True)  # Số điện thoại bàn
    mobile = models.CharField(max_length=15, blank=True, null=True) # Số di động
    # Liên kết khóa ngoại đến bảng Parent (nếu xóa Parent, set trường này thành NULL)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_join = models.DateField(auto_now_add=True) # Ngày tham gia (tự động lấy ngày tạo)
    status = models.BooleanField(default=True)         # Trạng thái hoạt động
    last_login_date = models.DateField(blank=True, null=True)
    last_login_ip = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        """Trả về tên đầy đủ của sinh viên"""
        return f"{self.fname} {self.lname}"
