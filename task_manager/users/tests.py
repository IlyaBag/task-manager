from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserTestCase(TestCase):
    """Testing CRUD operations with User model"""

    # fixtures = ['user.json']
    # username = 'oleguser'
    # password = 'oLe9$90v'
    
    # def example_test_index_page(self):
    #     response = self.client.get(reverse('users:index'))
    #     self.assertEqual(response.status_code, 200)

    def test_user_create(self):
        username = 'oleguser'
        first_name = 'Oleg'
        last_name = 'Olegov'
        password = 'oLe9$90v'

        response = self.client.post(
            reverse('user_create'),
            data={'username': username,
                  'first_name': first_name,
                  'last_name': last_name,
                  'password1': password,
                  'password2': password}
        )

        self.assertRedirects(response, reverse('user_login'), 302)

        new_user = User.objects.get(username=username)

        self.assertEqual(new_user.username, username, 'username is incorrect')
        self.assertEqual(new_user.first_name, first_name, 'first_name is incorrect')
        self.assertEqual(new_user.last_name, last_name, 'last_name is incorrect')

    def test_user_update(self):
        username = 'oleguser'
        first_name = 'Oleg'
        last_name = 'Olegov'
        password = 'oLe9$90v'

        self.client.post(
            reverse('user_create'),
            data={'username': username,
                  'first_name': first_name,
                  'last_name': last_name,
                  'password1': password,
                  'password2': password}
        )

        self.client.post(
            reverse('user_login'),
            data={'username': username,
                  'password': password}
        )

        user = User.objects.get(username=username)
        
        changed_first_name = 'Ivan'
        response = self.client.post(
            reverse('user_update', kwargs={'pk': user.pk}),
            data={'username': username,
                  'first_name': changed_first_name,
                  'last_name': last_name,
                  'password1': password,
                  'password2': password}
        )

        self.assertRedirects(response, reverse('users'), 302)

        user.refresh_from_db()
        self.assertEqual(user.first_name, changed_first_name)

    def test_user_delete(self):
        username = 'oleguser'
        first_name = 'Oleg'
        last_name = 'Olegov'
        password = 'oLe9$90v'

        self.client.post(
            reverse('user_create'),
            data={'username': username,
                  'first_name': first_name,
                  'last_name': last_name,
                  'password1': password,
                  'password2': password}
        )

        self.client.post(
            reverse('user_login'),
            data={'username': username,
                  'password': password}
        )

        user = User.objects.get(username=username)

        response = self.client.post(
            reverse('user_delete', kwargs={'pk': user.pk})
        )

        self.assertRedirects(response, reverse('users'), 302)

        deleted_user = User.objects.filter(id=user.pk)
        self.assertNotIn(user.pk, deleted_user)
