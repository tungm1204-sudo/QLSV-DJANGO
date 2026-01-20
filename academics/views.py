from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course, Classroom, Grade
from .forms import CourseForm, ClassroomForm
from django.db.models import Q

class CourseListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Course
    template_name = 'academics/course_list.html'
    context_object_name = 'courses'
    permission_required = 'academics.view_course'

    def get_queryset(self):
        query = self.request.GET.get('q')
        grade_id = self.request.GET.get('grade')
        queryset = Course.objects.select_related('grade').all()
        if query:
            queryset = queryset.filter(name__icontains=query)
        if grade_id:
            queryset = queryset.filter(grade_id=grade_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = Grade.objects.all()
        return context

class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'academics/course_form.html'
    success_url = reverse_lazy('academics:course_list')
    permission_required = 'academics.add_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Course'
        return context

class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'academics/course_form.html'
    success_url = reverse_lazy('academics:course_list')
    permission_required = 'academics.change_course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Course'
        return context

class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = 'academics/course_confirm_delete.html'
    success_url = reverse_lazy('academics:course_list')
    permission_required = 'academics.delete_course'

class ClassroomListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Classroom
    template_name = 'academics/classroom_list.html'
    context_object_name = 'classrooms'
    permission_required = 'academics.view_classroom'

    def get_queryset(self):
        query = self.request.GET.get('q')
        grade_id = self.request.GET.get('grade')
        year = self.request.GET.get('year')
        queryset = Classroom.objects.select_related('grade', 'teacher').all()
        if query:
            queryset = queryset.filter(
                Q(section__icontains=query) |
                Q(teacher__fname__icontains=query) |
                Q(teacher__lname__icontains=query)
            )
        if grade_id:
            queryset = queryset.filter(grade_id=grade_id)
        if year:
            queryset = queryset.filter(year=year)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = Grade.objects.all()
        context['years'] = Classroom.objects.values_list('year', flat=True).distinct().order_by('-year')
        return context

class ClassroomCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'academics/classroom_form.html'
    success_url = reverse_lazy('academics:classroom_list')
    permission_required = 'academics.add_classroom'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Classroom'
        return context

class ClassroomUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'academics/classroom_form.html'
    success_url = reverse_lazy('academics:classroom_list')
    permission_required = 'academics.change_classroom'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Classroom'
        return context

class ClassroomDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Classroom
    template_name = 'academics/classroom_confirm_delete.html'
    success_url = reverse_lazy('academics:classroom_list')
    permission_required = 'academics.delete_classroom'
