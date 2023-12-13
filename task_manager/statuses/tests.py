from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import StatusModel


class StatusTestCase(TestCase):
    """Testing CRUD operations with Status model"""
    # fixtures = ['user.json']
    username = 'oleguser'
    password = 'oLe9$90v'

    def setUp(self) -> None:
        self.client.post(
            reverse('user_create'),
            data={'username': self.username,
                  'password1': self.password,
                  'password2': self.password}
        )

        self.client.post(
            reverse('user_login'),
            data={'username': self.username,
                  'password': self.password}
        )

    def test_status_create(self):
        name = 'In progress'

        response = self.client.post(
            reverse('status_create'),
            data={'name': name}
        )

        self.assertRedirects(response, reverse('statuses'), 302)

        status = StatusModel.objects.get(name=name)

        self.assertEqual(status.name, name)
        self.assertIsInstance(status.created_at, datetime)

    def test_status_update(self):
        name = 'In progress'

        self.client.post(
            reverse('status_create'),
            data={'name': name}
        )

        status = StatusModel.objects.get(name=name)

        changed_name = 'Finished'
        response = self.client.post(
            reverse('status_update', kwargs={'pk': status.pk}),
            data={'name': changed_name}
        )

        self.assertRedirects(response, reverse('statuses'), 302)

        status.refresh_from_db()
        self.assertEqual(status.name, changed_name)

    def test_status_delete(self):
        name = 'In progress'

        self.client.post(
            reverse('status_create'),
            data={'name': name}
        )

        status = StatusModel.objects.get(name=name)

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': status.pk})
        )

        self.assertRedirects(response, reverse('statuses'), 302)

        deleted_status_qs = StatusModel.objects.filter(name=name)
        self.assertTrue(len(deleted_status_qs) == 0)

    def test_status_login_required(self):
        """
        Сhecking that only authorized users can perform actions with statuses.
        """
        self.client.post(reverse('user_logout'))

        # View status list
        url = reverse('statuses')
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"{reverse('user_login')}?next={url}",
            status_code=302,
            msg_prefix='Test for a status list'
        )

        # Status creating
        url = reverse('status_create')
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"{reverse('user_login')}?next={url}",
            status_code=302,
            msg_prefix='Test of a status creating'
        )

        # Status updating
        url = reverse('status_update', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"{reverse('user_login')}?next={url}",
            status_code=302,
            msg_prefix='Test of a status updating'
        )

        # Status deleting
        url = reverse('status_delete', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"{reverse('user_login')}?next={url}",
            status_code=302,
            msg_prefix='Test of a status deleting'
        )
