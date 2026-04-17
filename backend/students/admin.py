from django.contrib import admin
from .models import Parent, StudentProfile

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("fname", "lname", "mobile", "status")

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "mssv", "dob", "gender", "status")
