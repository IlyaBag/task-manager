from django import forms
from django.utils.translation import gettext_lazy as _
import django_filters

from task_manager.labels.models import LabelModel
from task_manager.tasks.models import TaskModel


class TaskFilter(django_filters.FilterSet):

    class Meta:
        model = TaskModel
        fields = ['status', 'executor']

    label = django_filters.ModelChoiceFilter(
        queryset=LabelModel.objects.all(),
        field_name='labels',
        label=_('Label')
    )
    self_tasks = django_filters.BooleanFilter(
        field_name='author_id',
        label=_('Self tasks only'),
        method='filter_self_tasks',
        widget=forms.CheckboxInput
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author_id=self.request.user)
        return queryset
