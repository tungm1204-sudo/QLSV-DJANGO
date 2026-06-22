from django.contrib import admin
from .models import TuitionConfig, TuitionFee, TuitionFeeDetail

@admin.register(TuitionConfig)
class TuitionConfigAdmin(admin.ModelAdmin):
    list_display = ('cost_per_credit', 'effective_date')

class TuitionFeeDetailInline(admin.TabularInline):
    model = TuitionFeeDetail
    extra = 0

@admin.register(TuitionFee)
class TuitionFeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'total_credits', 'total_amount', 'status', 'due_date')
    list_filter = ('status', 'semester')
    search_fields = ('student__mssv', 'student__user__first_name', 'student__user__last_name')
    inlines = [TuitionFeeDetailInline]
