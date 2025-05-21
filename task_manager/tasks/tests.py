from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status

from .models import Task


class TaskCrudTest(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpass123",
            first_name="Test",
            last_name="User1",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpass123",
            first_name="Test",
            last_name="User2",
        )

        # Create test status
        self.status = Status.objects.create(name="Test Status")

        # Create test task
        self.task = Task.objects.create(
            name="Test Task",
            description="Test description",
            status=self.status,
            creator=self.user1,
            executor=self.user2,
        )

    def test_task_list_view(self):
        # Log in
        self.client.login(username="testuser1", password="testpass123")

        # Access task list page
        response = self.client.get(reverse("tasks"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")

    def test_task_detail_view(self):
        # Log in
        self.client.login(username="testuser1", password="testpass123")

        # Access task detail page
        response = self.client.get(reverse("task_detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")
        self.assertContains(response, "Test description")

    def test_task_create_view(self):
        # Log in
        self.client.login(username="testuser1", password="testpass123")

        # Send POST request to create a task
        response = self.client.post(
            reverse("task_create"),
            {
                "name": "New Task",
                "description": "New description",
                "status": self.status.id,
                "executor": self.user2.id,
            },
            follow=True,
        )

        # Check if task was created
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_view(self):
        # Log in
        self.client.login(username="testuser1", password="testpass123")

        # Send POST request to update a task
        response = self.client.post(
            reverse("task_update", args=[self.task.id]),
            {
                "name": "Updated Task",
                "description": "Updated description",
                "status": self.status.id,
                "executor": self.user2.id,
            },
            follow=True,
        )

        # Check if task was updated
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")

    def test_task_delete_view_by_creator(self):
        # Log in as creator
        self.client.login(username="testuser1", password="testpass123")

        # Send POST request to delete a task
        response = self.client.post(
            reverse("task_delete", args=[self.task.id]), follow=True
        )

        # Check if task was deleted
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_delete_view_not_by_creator(self):
        # Log in as non-creator
        self.client.login(username="testuser2", password="testpass123")

        # Send POST request to delete a task
        response = self.client.post(
            reverse("task_delete", args=[self.task.id]), follow=True
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
        self.assertTrue(
            any(
                "Задачу может удалить только ее автор" in str(message)
                for message in messages
            )
        )

    def test_authentication_required(self):
        # Logout
        self.client.logout()

        # Try to access task pages without login
        urls = [
            reverse("tasks"),
            reverse("task_create"),
            reverse("task_detail", args=[self.task.id]),
            reverse("task_update", args=[self.task.id]),
            reverse("task_delete", args=[self.task.id]),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 302
            )  # Redirect to login page
