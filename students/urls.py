from django.urls import path
from . import views

app_name = 'students' # Tên namespace cho app, dùng trong template: {% url 'students:student_list' %}

urlpatterns = [
    # Trang danh sách sinh viên
    path('', views.StudentListView.as_view(), name='student_list'),
    
    # Trang thêm sinh viên mới
    path('add/', views.StudentCreateView.as_view(), name='student_create'),
    
    # Trang chỉnh sửa sinh viên (cần ID của sinh viên)
    path('<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_update'),
    
    # Trang xóa sinh viên (cần ID của sinh viên)
    path('<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
]
