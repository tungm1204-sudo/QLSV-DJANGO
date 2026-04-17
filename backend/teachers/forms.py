from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    """
    Form quản lý thông tin Giáo viên.
    """
    class Meta:
        model = Teacher
        fields = '__all__' # Sử dụng tất cả các trường trong model
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}), # Chọn ngày sinh
            'last_login_date': forms.DateInput(attrs={'type': 'date'}),
        }
