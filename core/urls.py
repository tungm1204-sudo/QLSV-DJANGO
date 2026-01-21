from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Đường dẫn trang chủ (Dashboard)
    path('', views.dashboard, name='dashboard'),
]
