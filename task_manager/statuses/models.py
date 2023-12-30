from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class StatusModel(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    created_at = models.DateTimeField(_('Creation date'), auto_now_add=True)

    def get_absolute_url(self):
        return reverse('statuses')

    def __str__(self) -> str:
        return self.name
