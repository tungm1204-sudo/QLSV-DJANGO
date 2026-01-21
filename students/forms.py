from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    """
    Form xử lý dữ liệu Sinh viên (Tạo mới & Cập nhật).
    Sử dụng ModelForm để map trực tiếp với model Student.
    """
    class Meta:
        model = Student
        fields = ['student_id', 'fname', 'lname', 'email', 'password', 'dob', 'phone', 'mobile', 'parent', 'status']
        # Định nghĩa các widget (giao diện nhập liệu) cho từng trường
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), # Input chọn ngày tháng
            'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), # Ẩn ký tự nhập vào
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile'}),
            'parent': forms.Select(attrs={'class': 'form-control'}), # Dropdown chọn phụ huynh
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}), # Checkbox trạng thái
        }
