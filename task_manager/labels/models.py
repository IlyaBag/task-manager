from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import TaskModel


class LabelModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    tasks = models.ManyToManyField(TaskModel)

    def get_absolute_url(self):
        return reverse('labels')

    def __str__(self) -> str:
        return self.name
