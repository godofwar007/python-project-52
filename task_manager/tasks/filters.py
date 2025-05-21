import django_filters
from django import forms
from django.contrib.auth.models import User

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from .models import Task


class TaskFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        executor_field = self.form.fields.get("executor")
        if executor_field:
            executor_field.label_from_instance = self.format_executor_label

    def format_executor_label(self, user):

        full_name = user.get_full_name().strip()
        if full_name:
            return full_name
        return user.username

    class Meta:
        model = Task
        fields = ["status", "executor", "labels", "self_tasks"]

    status = django_filters.ModelChoiceFilter(
        label=("Статус"),
        queryset=Status.objects.all(),
    )

    executor = django_filters.ModelChoiceFilter(
        label=("Исполнитель"),
        queryset=User.objects.all(),
    )

    labels = django_filters.ModelChoiceFilter(
        label=("Метка"),
        queryset=Label.objects.all(),
        method="filter_by_labels",
    )

    self_tasks = django_filters.BooleanFilter(
        label=("Только свои задачи"),
        method="filter_self_tasks",
        widget=forms.CheckboxInput,
    )

    def filter_by_labels(self, queryset, name, value):
        if value:
            return queryset.filter(labels=value)
        return queryset

    def filter_self_tasks(self, queryset, name, value):
        if value and hasattr(self, "request"):
            return queryset.filter(creator=self.request.user)
        return queryset
