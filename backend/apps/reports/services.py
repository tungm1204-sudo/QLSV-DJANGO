from django.db.models import Count, Sum, Q, Avg
from django.db import models
from apps.hr.models import Student, Lecturer
from apps.curriculum.models import CourseOffering
from apps.finance.models import StudentDebt, Receipt
from apps.exams.models import StudentAcademicRecord, ExamSession
from apps.graduation.models import Diploma
import pandas as pd
import io
import logging

logger = logging.getLogger(__name__)


def get_dashboard_stats(user):
    """
    Lấy số liệu tổng quan (Dashboard).
    WHY: Dùng aggregate một lần thay vì nhiều query riêng lẻ.
    """
    total_students = Student.objects.filter(status='STUDYING').count()
    total_lecturers = Lecturer.objects.filter(status='ACTIVE').count()

    # Doanh thu (tổng học phí đã đóng)
    total_revenue = Receipt.objects.filter(status='COMPLETED').aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Nợ (tổng học phí chưa đóng/quá hạn)
    total_debt = StudentDebt.objects.filter(status__in=['UNPAID', 'PARTIAL', 'OVERDUE']).aggregate(
        total=Sum(models.F('final_amount') - models.F('paid_amount'))
    )['total'] or 0

    active_classes = CourseOffering.objects.filter(status__in=['OPEN', 'IN_PROGRESS']).count()
    graduated_students = Student.objects.filter(status='GRADUATED').count()

    # Chart data
    chart_students_by_status = list(Student.objects.values('status').annotate(total=Count('id')))
    chart_students_by_major = list(Student.objects.values('major__name').annotate(total=Count('id')))
    chart_students_by_cohort = list(Student.objects.values('administrative_class__cohort__name').annotate(total=Count('id')))

    return {
        'total_students': total_students,
        'total_lecturers': total_lecturers,
        'total_revenue': total_revenue,
        'total_debt': total_debt,
        'active_classes': active_classes,
        'graduated_students': graduated_students,
        'chart_students_by_status': chart_students_by_status,
        'chart_students_by_major': chart_students_by_major,
        'chart_students_by_cohort': chart_students_by_cohort,
    }


def get_training_reports(filters):
    """
    Báo cáo đào tạo: Số lượng sinh viên theo khoa/ngành/khóa.
    WHY: Dùng select_related cho major và cohort để tránh N+1 khi render.
    """
    qs = Student.objects.select_related(
        'major__department', 'administrative_class__cohort'
    )
    if filters.get('department_id'):
        qs = qs.filter(major__department_id=filters['department_id'])
    if filters.get('major_id'):
        qs = qs.filter(major_id=filters['major_id'])
    if filters.get('cohort_id'):
        qs = qs.filter(administrative_class__cohort_id=filters['cohort_id'])

    stats = qs.values(
        'major__name', 'administrative_class__cohort__name'
    ).annotate(
        total=Count('id'),
        studying=Count('id', filter=Q(status='STUDYING')),
        graduated=Count('id', filter=Q(status='GRADUATED')),
        warning=Count('id', filter=Q(status='ACADEMIC_WARNING')),
    )
    return list(stats)


def get_academic_reports(filters):
    """
    Báo cáo học tập: Thống kê học lực theo kỳ/ngành.
    """
    qs = StudentAcademicRecord.objects.select_related('student__major', 'semester')
    if filters.get('semester_id'):
        qs = qs.filter(semester_id=filters['semester_id'])
    if filters.get('major_id'):
        qs = qs.filter(student__major_id=filters['major_id'])

    stats = qs.values('academic_classification').annotate(
        total=Count('id'),
        avg_gpa=Avg('semester_gpa'),
    )
    return list(stats)


def get_finance_reports(filters):
    """
    Báo cáo tài chính: Tổng thu, dư nợ theo ngành.
    WHY: select_related student__major tránh N+1 khi group-by tên ngành.
    """
    qs = StudentDebt.objects.select_related('student__major', 'semester')
    if filters.get('semester_id'):
        qs = qs.filter(semester_id=filters['semester_id'])

    stats = qs.values('student__major__name').annotate(
        total_tuition=Sum('final_amount'),
        total_paid=Sum('paid_amount'),
        total_debt=Sum(models.F('final_amount') - models.F('paid_amount'))
    )
    return list(stats)


def get_hr_reports(filters):
    """
    Báo cáo nhân sự: Số lượng giảng viên theo phòng ban.
    WHY: select_related department tránh N+1 khi group-by tên phòng ban.
    """
    qs = Lecturer.objects.select_related('department')
    if filters.get('department_id'):
        qs = qs.filter(department_id=filters['department_id'])

    stats = qs.values('department__name').annotate(
        total=Count('id')
    )
    return list(stats)


def get_exam_reports(filters):
    """
    Báo cáo khảo thí: Số kỳ thi, tỷ lệ đậu/rớt theo môn.
    """
    qs = ExamSession.objects.select_related('semester')
    if filters.get('semester_id'):
        qs = qs.filter(semester_id=filters['semester_id'])

    stats = qs.values('course__name').annotate(
        total_exams=Count('id')
    )
    return list(stats)


def export_report_to_excel(data: list, report_type: str) -> io.BytesIO:
    """
    Xuất dữ liệu báo cáo ra file Excel in-memory.
    WHY: Dùng pandas để có khả năng format + multi-sheet nếu cần mở rộng.
    """
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=report_type[:31])  # sheet name max 31 chars
    output.seek(0)
    return output


def export_report_to_pdf_html(data: list, report_type: str, title: str = '') -> str:
    """
    Tạo HTML report để in / convert thành PDF qua trình duyệt (window.print).
    WHY: Không cần cài thêm thư viện nặng (reportlab/wkhtmltopdf) — dùng HTML
    chuẩn, Frontend tự in hoặc dùng Puppeteer/Chrome headless nếu cần PDF thật.
    Trả về string HTML hoàn chỉnh.
    """
    if not title:
        title = report_type.replace('_', ' ').title()

    if not data:
        rows_html = '<tr><td colspan="100" style="text-align:center">Không có dữ liệu</td></tr>'
        headers_html = ''
    else:
        keys = list(data[0].keys())
        headers_html = ''.join(f'<th>{k}</th>' for k in keys)
        rows_html = ''.join(
            '<tr>' + ''.join(f'<td>{row.get(k, "")}</td>' for k in keys) + '</tr>'
            for row in data
        )

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; font-size: 13px; }}
        h2 {{ text-align: center; margin-bottom: 4px; }}
        p.subtitle {{ text-align: center; color: #555; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
        th {{ background: #2c5f8a; color: #fff; padding: 8px 10px; text-align: left; }}
        td {{ padding: 7px 10px; border-bottom: 1px solid #ddd; }}
        tr:nth-child(even) {{ background: #f5f8fc; }}
        .footer {{ margin-top: 30px; text-align: right; font-size: 11px; color: #888; }}
        @media print {{
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <h2>{title}</h2>
    <p class="subtitle">Báo cáo được tạo tự động bởi Hệ thống QLSV</p>
    <table>
        <thead><tr>{headers_html}</tr></thead>
        <tbody>{rows_html}</tbody>
    </table>
    <div class="footer">Xuất ngày: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
    <div class="no-print" style="margin-top:20px;text-align:center">
        <button onclick="window.print()" style="padding:8px 24px;cursor:pointer">🖨 In / Xuất PDF</button>
    </div>
</body>
</html>"""
    return html
