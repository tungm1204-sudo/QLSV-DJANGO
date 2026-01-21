from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    # Danh sách giáo viên
    path('', views.TeacherListView.as_view(), name='teacher_list'),
    
    # Thêm giáo viên
    path('create/', views.TeacherCreateView.as_view(), name='teacher_create'),
    
    # Cập nhật thông tin giáo viên
    path('<int:pk>/update/', views.TeacherUpdateView.as_view(), name='teacher_update'),
    
    # Xóa giáo viên
    path('<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher_delete'),
]
