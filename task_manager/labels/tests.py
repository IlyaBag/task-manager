from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import LabelModel


class LabelsTestCase(TestCase):
    """Testing CRUD operations with Label model"""
    username = 'oleguser'
    password = 'oLe9$90v'
    label_name = 'Important'

    def setUp(self) -> None:
        self.client.post(
            reverse('user_create'),
            data={'username': self.username,
                  'password1': self.password,
                  'password2': self.password}
        )

        self.client.login(username=self.username, password=self.password)

        self.client.post(
            reverse('label_create'),
            data={'name': self.label_name}
        )

    def test_label_create(self):
        name = 'test_label'

        response = self.client.post(
            reverse('label_create'),
            data={'name': name}
        )

        self.assertRedirects(response, reverse('labels'), 302)

        label = LabelModel.objects.get(name=name)

        self.assertEqual(label.name, name)
        self.assertIsInstance(label.created_at, datetime)

    def test_label_update(self):
        label = LabelModel.objects.get(name=self.label_name)

        changed_name = 'Fix'
        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.pk}),
            data={'name': changed_name}
        )

        self.assertRedirects(response, reverse('labels'), 302)

        label.refresh_from_db()
        self.assertEqual(label.name, changed_name)

    def test_label_delete(self):
        label = LabelModel.objects.get(name=self.label_name)

        response = self.client.post(
            reverse('label_delete', kwargs={'pk': label.pk})
        )

        self.assertRedirects(response, reverse('labels'), 302)

        all_labels = LabelModel.objects.all()
        self.assertNotIn(label, all_labels)
