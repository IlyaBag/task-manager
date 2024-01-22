from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import LabelModel


class LabelsTestCase(TestCase):
    """Testing CRUD operations with Label model"""
    USERNAME = 'oleguser'
    PASSWORD = 'oLe9$90v'
    LABEL_NAME = 'Important'

    def setUp(self) -> None:
        self.client.post(
            reverse('user_create'),
            data={'username': self.USERNAME,
                  'password1': self.PASSWORD,
                  'password2': self.PASSWORD}
        )

        self.client.login(username=self.USERNAME, password=self.PASSWORD)

        self.client.post(
            reverse('label_create'),
            data={'name': self.LABEL_NAME}
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

    def test_label_update(self):
        label = LabelModel.objects.get(name=self.LABEL_NAME)

        changed_name = 'Fix'
        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.pk}),
            data={'name': changed_name}
        )

        self.assertRedirects(response, reverse('labels'), 302)

        label.refresh_from_db()
        self.assertEqual(label.name, changed_name)

    def test_label_delete(self):
        label = LabelModel.objects.get(name=self.LABEL_NAME)

        response = self.client.post(
            reverse('label_delete', kwargs={'pk': label.pk})
        )

        self.assertRedirects(response, reverse('labels'), 302)

        all_labels = LabelModel.objects.all()
        self.assertNotIn(label, all_labels)


class LabelsRestrictionTestCase(TestCase):
    """You cannot delete a label if it is associated with a task."""
    USERNAME = 'oleguser'
    PASSWORD = 'oLe9$90v'
    LABEL_NAME = 'Important'

    def setUp(self) -> None:
        self.client.post(
            reverse('user_create'),
            data={'username': self.USERNAME,
                  'password1': self.PASSWORD,
                  'password2': self.PASSWORD}
        )

        self.client.login(username=self.USERNAME, password=self.PASSWORD)

        self.client.post(
            reverse('label_create'),
            data={'name': self.LABEL_NAME}
        )

        self.client.post(
            reverse('status_create'),
            {'name': 'testing'}
        )

        self.client.post(
            reverse('task_create'),
            {
                'name': 'Taskname',
                'status': 1,
                'labels': 1
            }
        )

    def test_label_delete_prohibited(self):
        label = LabelModel.objects.get(name=self.LABEL_NAME)

        response = self.client.post(reverse('label_delete', kwargs={'pk': 1}))

        self.assertRedirects(response, reverse('labels'), 302)

        all_labels = LabelModel.objects.all()
        self.assertIn(label, all_labels)
