from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks/tasks.html"
    context_object_name = "tasks"
    login_url = reverse_lazy("login")
    filterset_class = TaskFilter


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/create.html"
    success_url = reverse_lazy("tasks")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        messages.success(self.request, ("Задача успешно создана"))
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/update.html"
    success_url = reverse_lazy("tasks")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, ("Задача успешно изменена"))
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/delete.html"
    success_url = reverse_lazy("tasks")
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.get_object().creator == self.request.user

    def form_valid(self, form):
        messages.success(self.request, ("Задача успешно удалена"))
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(
            self.request, ("Задачу может удалить только ее автор")
        )
        return redirect("tasks")


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/details.html"
    context_object_name = "task"
    login_url = reverse_lazy("login")
