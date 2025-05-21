from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserCRUDTests(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(
            username='existing', password='StrongPass123',
            first_name='Exist', last_name='User'
        )

    def test_user_registration_redirects_to_login(self):
        url = reverse('user_create')
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update_redirects_to_users_list(self):
        self.client.force_login(self.existing_user)
        url = reverse('user_update', args=[self.existing_user.id])
        data = {
            'first_name': 'Changed',
            'last_name': 'Name',
            'username': 'existing',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('users'))
        self.existing_user.refresh_from_db()
        self.assertEqual(self.existing_user.first_name, 'Changed')
        self.assertEqual(self.existing_user.last_name, 'Name')

    def test_user_delete_redirects_to_users_list(self):
        self.client.force_login(self.existing_user)
        url = reverse('user_delete', args=[self.existing_user.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users'))
        self.assertFalse(User.objects.filter(username='existing').exists())

    def test_user_login_redirects_to_home(self):
        url = reverse('login')
        data = {
            'username': 'existing',
            'password': 'StrongPass123',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('home'))
