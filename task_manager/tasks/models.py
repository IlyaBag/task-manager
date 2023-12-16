from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

from task_manager.statuses.models import StatusModel


class TaskModel(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    description = models.TextField(_('Description'), null=True)  # необязательное
    status = models.ForeignKey(  # обязательное
        StatusModel,
        on_delete=models.PROTECT,
        verbose_name = _('Status')
    )
    # labels = models.ManyToManyField(
    #     "LabelModel"
    # )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('Executor')
    )
    author = models.ForeignKey(  # обязательное автоматом
        User,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('Author'),
        auto_created=True
    )
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True)
