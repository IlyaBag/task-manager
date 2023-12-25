from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import LabelModel
from task_manager.statuses.models import StatusModel


class TaskModel(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    description = models.TextField(_('Description'), blank=True)
    status = models.ForeignKey(
        StatusModel,
        on_delete=models.PROTECT,
        verbose_name = _('Status')
    )
    labels = models.ManyToManyField(
        LabelModel,
        verbose_name=_('Labels'),
        blank=True
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Executor'),
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('Author'),
        auto_created=True
    )
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True)

    def get_absolute_url(self):
        return reverse('tasks')
    
    def __str__(self) -> str:
        return self.name
    