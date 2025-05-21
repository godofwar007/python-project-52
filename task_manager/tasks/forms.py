from django import forms

from .models import Task


class TaskForm(forms.ModelForm):

    @staticmethod
    def _executor_label(user):
        full_name = f"{user.first_name} {user.last_name}".strip()
        return full_name or user.username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"].label_from_instance = self._executor_label

    class Meta:
        model = Task
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": "Имя",
            "description": "Описание",
            "status": "Статус",
            "executor": "Исполнитель",
            "labels": "Метки",
        }
