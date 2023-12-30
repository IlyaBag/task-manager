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


class TaskFiltersTestCase(TestCase):
    """Testing task list display filters"""
    username1 = 'User_one'
    username2 = 'User_two'
    password = 'qweruiop'

    status1 = 'New'
    status2 = 'In progress'

    label1 = 'bug'
    label2 = 'fix'
    label3 = 'check'

    task1 = {
        'name': 'Code',
        'status': 2,
        'labels': 1,
    }
    task2 = {
        'name': 'Test',
        'status': 2,
        'labels': [2, 3],
    }
    task3 = {
        'name': 'Deploy',
        'status': 1,
        'labels': 3,
    }

    def setUp(self) -> None:
        for username in [self.username1, self.username2]:
            self.client.post(
                reverse('user_create'),
                {
                    'username': username,
                    'password1': self.password,
                    'password2': self.password,
                }
            )
        self.client.login(username=self.username1, password=self.password)

        for status in [self.status1, self.status2]:
            self.client.post(
                reverse('status_create'),
                {'name': status}
            )

        for label in [self.label1, self.label2, self.label3]:
            self.client.post(
                reverse('label_create'),
                {'name': label}
            )

        self.client.post(
            reverse('task_create'),
            {**self.task1}
        )
        self.client.logout
        self.client.login(username=self.username2, password=self.password)
        for task in [self.task2, self.task3]:
            self.client.post(
                reverse('task_create'),
                {**task}
            )

    def test_status_filter(self):
        response = self.client.get(
            reverse('tasks'),
            QUERY_STRING='status=1'
        )
        self.assertContains(response, self.task3.get('name'))
        self.assertNotContains(response, self.task1.get('name'))
        self.assertNotContains(response, self.task2.get('name'))

    def test_label_filter(self):
        response = self.client.get(
            reverse('tasks'),
            QUERY_STRING='label=3'
        )
        self.assertContains(response, self.task2.get('name'))
        self.assertContains(response, self.task3.get('name'))
        self.assertNotContains(response, self.task1.get('name'))

    def test_self_tasks_filter(self):
        response = self.client.get(
            reverse('tasks'),
            QUERY_STRING='self_tasks=on'
        )
        current_user = response.wsgi_request.user
        current_user_tasks = TaskModel.objects.filter(author=current_user)
        other_tasks = TaskModel.objects.exclude(author=current_user)
        for task in current_user_tasks:
            self.assertContains(response, task.name)
        for task in other_tasks:
            self.assertNotContains(response, task.name)
