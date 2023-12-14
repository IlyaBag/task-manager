from typing import Any
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

from task_manager.statuses.models import StatusModel
from task_manager.users.mixins import CustomLoginRequiredMixin


class StatusesListView(CustomLoginRequiredMixin, TemplateView):
    """Provide a list of all existing statuses."""
    template_name = 'statuses/statuses-list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['statuses'] = StatusModel.objects.all()
        return context


class StatusCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new status."""
    model = StatusModel
    fields = ['name']
    template_name_suffix = '-create'
    success_message = _('Status successfully created')


class StatusUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update an existing status"""
    model = StatusModel
    fields = ['name']
    template_name_suffix = '-update'
    success_message = _('Status changed successfully')


class StatusDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete an existing status"""
    model = StatusModel
    template_name_suffix = '-delete'
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
