from django.apps import AppConfig


class AcademicsConfig(AppConfig):
    """
    App Configuration cho app 'academics'.
    Chứa các model liên quan đến quản lý học vụ: Học kỳ, Lớp học, Môn học, Điểm danh, Điểm thi.
    """
    name = 'academics'
