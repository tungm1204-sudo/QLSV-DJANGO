from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Student
from .forms import StudentForm
from django.db.models import Q

class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    permission_required = 'students.view_student'

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Student.objects.select_related('parent').all()
        if query:
            queryset = queryset.filter(
                Q(fname__icontains=query) | 
                Q(lname__icontains=query) | 
                Q(email__icontains=query)
            )
        return queryset

class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')
    permission_required = 'students.add_student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Student'
        return context

class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
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
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:student_list')
    permission_required = 'students.delete_student'
