from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import LabelModel
from task_manager.statuses.models import StatusModel


class TaskViewFilterForm(forms.Form):
    status = forms.ModelChoiceField(StatusModel.objects,
                                    label=_('Status'),
                                    required=False)
    executor = forms.ModelChoiceField(User.objects,
                                      label=_('Executor'),
                                      required=False)
    label = forms.ModelChoiceField(LabelModel.objects,
                                   label=_('Label'),
                                   required=False)
    self_tasks = forms.ChoiceField(widget=forms.CheckboxInput,
                                   label=_('Only your tasks'),
                                   required=False)
