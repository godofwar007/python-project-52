from django.contrib.auth.models import User
from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150, verbose_name="Name")
    description = models.TextField(blank=True, verbose_name="Description")
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name="Status"
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_tasks",
        verbose_name="Creator",
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="assigned_tasks",
        blank=True,
        null=True,
        verbose_name="Executor",
    )
    labels = models.ManyToManyField(
        Label, related_name="tasks", blank=True, verbose_name="Labels"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created at"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]
