from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    # Quản lý Môn học (Courses)
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
    # Quản lý Lớp học (Classrooms)
    path('classes/', views.ClassroomListView.as_view(), name='classroom_list'),
    path('classes/create/', views.ClassroomCreateView.as_view(), name='classroom_create'),
    path('classes/<int:pk>/update/', views.ClassroomUpdateView.as_view(), name='classroom_update'),
    path('classes/<int:pk>/delete/', views.ClassroomDeleteView.as_view(), name='classroom_delete'),
]
