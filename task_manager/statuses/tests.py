from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import StatusModel


class StatusTestCase(TestCase):
    """Testing CRUD operations with Status model"""
    fixtures = ['user.json']
    username = 'oleguser'
    password = 'oLe9$90v'

    def test_status_create(self):
        name = 'In progress'

        response = self.client.post(
            reverse('status_create'),
            data={'name': name}
        )

        self.assertRedirects(response, reverse('statuses_list'), 302)

        status = StatusModel.objects.get(name=name)

        self.assertEqual(status.name, name)
        self.assertIsInstance(status.created_at, datetime)

    def test_status_update(self):
        name = 'In progress'

        self.client.post(
            reverse('user_login'),
            data={'username': self.username,
                  'password': self.password}
        )

        self.client.post(
            reverse('status_create'),
            data={'name': name}
        )

        status = StatusModel.objects.get(name=name)

        changed_status = 'Finished'
        response = self.client.post(
            reverse('status_update', kwargs={'pk': status.pk}),
            data={'name': changed_status}
        )

        self.assertRedirects(response, reverse('statuses_list'), 302)

        status.refresh_from_db()
        self.assertEqual(status.name, changed_status)

    def test_status_delete(self):
        name = 'In progress'

        self.client.post(
            reverse('user_login'),
            data={'username': self.username,
                  'password': self.password}
        )

        self.client.post(
            reverse('status_create'),
            data={'name': name}
        )

        status = StatusModel.objects.get(name=name)

        response = self.client.post(
            reverse('status_delete', kwargs={'pk': status.pk})
        )

        self.assertRedirects(response, reverse('statuses_list'), 302)

        deleted_status = StatusModel.objects.filter(id=status.pk)
        self.assertNotIn(status.pk, deleted_status)
