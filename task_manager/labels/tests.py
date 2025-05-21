from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

from .models import Label


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.label = Label.objects.create(name="Test Label")
        self.status = Status.objects.create(name="Test Status")
        self.login_url = reverse("login")

    def test_label_list_view_requires_login(self):
        response = self.client.get(reverse("labels"))
        self.assertRedirects(
            response, f'{self.login_url}?next={reverse("labels")}'
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("labels"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels.html")

    def test_label_create_view(self):
        response = self.client.get(reverse("label_create"))
        self.assertRedirects(
            response, f'{self.login_url}?next={reverse("label_create")}'
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("label_create"), {"name": "New Label"}
        )
        self.assertRedirects(response, reverse("labels"))
        self.assertTrue(Label.objects.filter(name="New Label").exists())

    def test_label_update_view(self):
        response = self.client.get(
            reverse("label_update", args=[self.label.id])
        )
        next_url = reverse("label_update", args=[self.label.id])
        self.assertRedirects(response, f"{self.login_url}?next={next_url}")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("label_update", args=[self.label.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("label_update", args=[self.label.id]),
            {"name": "Updated Label"},
        )
        self.assertRedirects(response, reverse("labels"))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated Label")

    def test_label_delete_view(self):
        response = self.client.get(
            reverse("label_delete", args=[self.label.id])
        )
        next_url = reverse("label_delete", args=[self.label.id])
        self.assertRedirects(response, f"{self.login_url}?next={next_url}")
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("label_delete", args=[self.label.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("label_delete", args=[self.label.id])
        )
        self.assertRedirects(response, reverse("labels"))

        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_cannot_delete_label_in_use(self):
        self.client.login(username="testuser", password="testpassword")
        task = Task.objects.create(
            name="Test Task",
            description="Test description",
            status=self.status,
            creator=self.user,
        )
        task.labels.add(self.label)
        response = self.client.post(
            reverse("label_delete", args=[self.label.id])
        )
        self.assertRedirects(response, reverse("labels"))
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
