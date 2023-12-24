from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class LabelModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True)

    def get_absolute_url(self):
        return reverse('labels')

    def __str__(self) -> str:
        return self.name
