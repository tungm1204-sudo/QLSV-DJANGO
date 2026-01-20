from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Teacher
from .forms import TeacherForm
from django.db.models import Q

class TeacherListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'
    permission_required = 'teachers.view_teacher'

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Teacher.objects.all()
        if query:
            queryset = queryset.filter(
                Q(fname__icontains=query) | 
                Q(lname__icontains=query) | 
                Q(email__icontains=query)
            )
        return queryset

class TeacherCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teachers:teacher_list')
    permission_required = 'teachers.add_teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Teacher'
        return context

class TeacherUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'teachers/teacher_form.html'
    success_url = reverse_lazy('teachers:teacher_list')
    permission_required = 'teachers.change_teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Teacher'
        return context

class TeacherDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'teachers/teacher_confirm_delete.html'
    success_url = reverse_lazy('teachers:teacher_list')
    permission_required = 'teachers.delete_teacher'
