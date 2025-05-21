from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/labels.html"
    context_object_name = "labels"
    login_url = reverse_lazy("login")


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/create.html"
    success_url = reverse_lazy("labels")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, ("Метка успешно создана"))
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "labels/update.html"
    success_url = reverse_lazy("labels")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, ("Метка успешно изменена"))
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "labels/delete.html"
    success_url = reverse_lazy("labels")
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(
                self.request, (
                    "Невозможно удалить метку, потому что она используется")
            )
            return redirect("labels")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, ("Метка успешно удалена"))
        return super().form_valid(form)
