from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Student
from .forms import StudentForm
from django.db.models import Q

class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    View hiển thị danh sách tất cả sinh viên.
    Yêu cầu đăng nhập và quyền xem sinh viên.
    """
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students' # Tên biến context sử dụng trong template
    permission_required = 'students.view_student' # Quyền bắt buộc

    def get_queryset(self):
        """
        Ghi đè phương thức lấy dữ liệu để hỗ trợ tìm kiếm (Search).
        """
        query = self.request.GET.get('q') # Lấy từ khóa tìm kiếm từ URL (param 'q')
        # Tối ưu truy vấn bằng select_related để lấy luôn thông tin Parent
        queryset = Student.objects.select_related('parent').all()
        
        if query:
            # Lọc theo Tên HOẶC Họ HOẶC Email (không phân biệt hoa thường)
            queryset = queryset.filter(
                Q(fname__icontains=query) | 
                Q(lname__icontains=query) | 
                Q(email__icontains=query)
            )
        return queryset

class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    View tạo mới một sinh viên.
    """
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list') # Chuyển hướng sau khi tạo thành công
    permission_required = 'students.add_student'
    
    def get_context_data(self, **kwargs):
        """Thêm tiêu đề trang vào context"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Student'
        return context

class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    View cập nhật thông tin sinh viên hiện có.
    """
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')
    permission_required = 'students.change_student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Student'
        return context

class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    View xóa sinh viên. 
    Hiển thị trang xác nhận trước khi xóa thật sự.
    """
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:student_list')
    permission_required = 'students.delete_student'
