from typing import Any
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from task_manager.tasks.filters import TaskFilter

from task_manager.tasks.models import TaskModel
from task_manager.users.mixins import CustomLoginRequiredMixin


class TasksListView(CustomLoginRequiredMixin, TemplateView):
    """Show list of all tasks."""
    template_name = 'tasks/tasks-list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        filter = TaskFilter(data=self.request.GET,
                            queryset=TaskModel.objects.all(),
                            request=self.request)
        context['form'] = filter.form
        context['tasks'] = filter.qs
        return context


class TaskInfoView(CustomLoginRequiredMixin, TemplateView):
    """Show information about a single task."""
    template_name = 'tasks/task-info.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        task_id = context.get('pk')
        context['task'] = TaskModel.objects.get(pk=task_id)
        return context


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new task."""
    model = TaskModel
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name_suffix = '-create'
    success_message = _('Task successfully created')

    def form_valid(self, form):
        """
        If the form is valid, add current user to "author" field 
        and save the associated model.
        """
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)



class TaskUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update an existing task."""
    model = TaskModel
    fields = ['name', 'description', 'status', 'executor', 'labels']
    template_name_suffix = '-update'
    success_message = _('Task changed successfully')


class TaskDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete an existing task. Only the author of a task can delete it."""
    model = TaskModel
    template_name_suffix = '-delete'
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        task_id = kwargs.get('pk')
        task = TaskModel.objects.get(id=task_id)
        if request.user.id != task.author.id:
            messages.error(request, _('Only the author of a task can delete it'))
            return redirect(reverse_lazy('tasks'))
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        task_id = kwargs.get('pk')
        task = TaskModel.objects.get(id=task_id)
        if request.user.id != task.author.id:
            return redirect(reverse_lazy('tasks'))
        return super().post(request, *args, **kwargs)
