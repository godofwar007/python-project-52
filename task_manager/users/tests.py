from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserTests(TestCase):

    def test_user_registration(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'testuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_update(self):
        user = User.objects.create_user(username='user1', password='pass')
        self.client.force_login(user)
        response = self.client.post(reverse('user_update', args=[user.id]), {
            'username': 'updated_user',
            'email': 'user@example.com'
        })
        self.assertRedirects(response, reverse('users')
                             )
        user.refresh_from_db()
        self.assertEqual(user.username, 'updated_user')

    def test_user_delete(self):
        user = User.objects.create_user(username='user2', password='pass')
        self.client.force_login(user)
        response = self.client.post(reverse('user_delete', args=[user.id]))
        self.assertRedirects(response, reverse('users')
                             )
        self.assertFalse(User.objects.filter(username='user2').exists())
