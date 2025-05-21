from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import StatusForm
from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/statuses.html"
    context_object_name = "statuses"
    login_url = reverse_lazy("login")


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, ("Статус успешно создан"))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, ("Статус успешно изменен"))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, ("Статус успешно удален"))
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if status.task_set.exists():
            messages.error(
                self.request, (
                    "Невозможно удалить статус, потому что он используется")
            )
            return redirect("statuses")
        return super().post(request, *args, **kwargs)
