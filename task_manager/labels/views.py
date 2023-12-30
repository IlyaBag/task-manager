from typing import Any

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from task_manager.labels.models import LabelModel
from task_manager.users.mixins import CustomLoginRequiredMixin


class LabelsListView(CustomLoginRequiredMixin, TemplateView):
    """Provide a list of all existing labels."""
    template_name = 'labels/labels-list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['labels'] = LabelModel.objects.all()
        return context


class LabelCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new label."""
    model = LabelModel
    fields = ['name']
    template_name_suffix = '-create'
    success_message = _('Label successfully created')


class LabelUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update an existing label."""
    model = LabelModel
    fields = ['name']
    template_name_suffix = '-update'
    success_message = _('Label changed successfully')


class LabelDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete an existing label."""
    model = LabelModel
    template_name_suffix = '-delete'
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully deleted')

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """It is forbidden to delete tags assigned to at least one task."""
        label = LabelModel.objects.get(id=self.object.pk)
        if label.taskmodel_set.count() > 0:
            messages.error(
                self.request,
                _('Cannot remove label because it is in use')
            )
            return redirect('labels')
        return super().form_valid(form)
