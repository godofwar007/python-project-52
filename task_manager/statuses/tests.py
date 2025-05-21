from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.status = Status.objects.create(name="Test Status")

        self.login_url = reverse("login")

    def test_status_list_view_requires_login(self):
        response = self.client.get(reverse("statuses"))
        self.assertRedirects(
            response, f'{self.login_url}?next={reverse("statuses")}'
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("statuses"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses.html")

    def test_status_create_view(self):
        response = self.client.get(reverse("status_create"))
        self.assertRedirects(
            response, f'{self.login_url}?next={reverse("status_create")}'
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("status_create"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("status_create"), {"name": "New Status"}
        )
        self.assertRedirects(response, reverse("statuses"))

        self.assertTrue(Status.objects.filter(name="New Status").exists())

    def test_status_update_view(self):
        response = self.client.get(
            reverse("status_update", args=[self.status.id])
        )
        next_url = reverse("status_update", args=[self.status.id])
        self.assertRedirects(response, f"{self.login_url}?next={next_url}")

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("status_update", args=[self.status.id])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("status_update", args=[self.status.id]),
            {"name": "Updated Status"},
        )
        self.assertRedirects(response, reverse("statuses"))

        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated Status")

    def test_status_delete_view(self):
        response = self.client.get(
            reverse("status_delete", args=[self.status.id])
        )
        next_url = reverse("status_delete", args=[self.status.id])
        self.assertRedirects(response, f"{self.login_url}?next={next_url}")

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("status_delete", args=[self.status.id])
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("status_delete", args=[self.status.id])
        )
        self.assertRedirects(response, reverse("statuses"))

        self.assertFalse(Status.objects.filter(id=self.status.id).exists())
