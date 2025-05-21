from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            verbose_name="name")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="сreated at"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Label"
        verbose_name_plural = "Labels"
        ordering = ["name"]
