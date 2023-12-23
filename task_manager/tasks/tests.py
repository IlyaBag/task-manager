from django.test import TestCase
from django.urls import reverse

from task_manager.tasks.models import TaskModel


class TaskTestCase(TestCase):
    """Testing CRUD operations with Task model"""
    def setUp(self) -> None:
        username = 'oleguser'
        password = 'oLe9$90v'

        self.client.post(
            reverse('user_create'),
            data={'username': username,
                  'password1': password,
                  'password2': password}
        )
        self.client.login(username=username, password=password)

        self.client.post(
            reverse('status_create'),
            data={'name': 'testing'}
        )

        name = 'Use TDD'
        description = 'Write tests for CRUD operations'
        status_id = 1
        executor_id = 1
        author_id = 1

        self.client.post(
            reverse('task_create'),
            data={'name': name,
                  'description': description,
                  'status': status_id,
                  'executor': executor_id,
                  'author': author_id}
        )

    def test_task_create(self):
        name = 'Test task creation'
        description = 'Write a test to check correct task creation'
        status_id = 1
        executor_id = 1

        self.client.post(
            reverse('task_create'),
            data={'name': name,
                  'description': description,
                  'status': status_id,
                  'author': executor_id,
                  'executor': executor_id}
        )

        task = TaskModel.objects.get(name=name)

        self.assertEqual(task.description, description)
        self.assertEqual(task.status.name, 'testing')
        self.assertEqual(task.author.username, 'oleguser')
        self.assertEqual(task.executor.username, 'oleguser')

    def test_task_update(self):
        task = TaskModel.objects.get(name='Use TDD')

        self.client.post(
            reverse('task_update', kwargs={'pk': task.pk}),
            data={'name': task.name,
                  'description': 'new description',
                  'status': task.status_id,
                  'author': task.executor_id,
                  'executor': task.executor_id}
        )

        changed_task = TaskModel.objects.get(name=task.name)

        self.assertEqual(changed_task.description, 'new description')
        self.assertEqual(task.id, changed_task.id)
        self.assertEqual(task.name, changed_task.name)
        self.assertEqual(task.created_at, changed_task.created_at)

    def test_task_delete(self):
        task = TaskModel.objects.get(name='Use TDD')

        self.client.post(reverse('task_delete', kwargs={'pk': task.pk}))

        all_tasks = TaskModel.objects.all()

        self.assertNotIn(task, all_tasks)

    def test_task_delete_only_by_author(self):
        self.client.logout()
        self.client.post(
            reverse('user_create'),
            data={'username': 'not_author',
                  'password1': 'password',
                  'password2': 'password'}
        )
        self.client.login(username='not_author', password='password')

        task = TaskModel.objects.get(name='Use TDD')

        self.client.post(reverse('task_delete', kwargs={'pk': task.pk}))

        all_tasks = TaskModel.objects.all()

        self.assertIn(task, all_tasks)
