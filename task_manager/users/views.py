from typing import Any

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from task_manager.users.forms import UserCreateForm, UserUpdateForm
from task_manager.users.mixins import CustomLoginRequiredMixin


class UsersView(TemplateView):
    """Provide a list of all registered users."""

    template_name = 'users/users-list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class UserCreateView(SuccessMessageMixin, CreateView):
    """Register a new user."""
    template_name = 'users/user-create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('user_login')
    success_message = _('User successfully registered')


class UserUpdateView(CustomLoginRequiredMixin, View):
    """Update an info in user`s profile."""

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')

        if user_id == request.user.id:
            user = User.objects.get(id=user_id)
            form = UserUpdateForm(instance=user)
            return render(request, 'users/user-update.html', {'form': form})

        messages.add_message(
            request,
            messages.ERROR,
            _('You do not have permission to change another user.')
        )
        return redirect('users')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('User successfully updated'))
            return redirect('users')
        return render(request, 'users/user-update.html', {'form': form})


class UserDeleteView(CustomLoginRequiredMixin, View):
    """Delete an existing user."""

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if user_id == request.user.id:
            user = User.objects.get(id=user_id)
            return render(request, 'users/user-delete.html', {'user': user})
        messages.add_message(
            request,
            messages.ERROR,
            _('You do not have permission to change another user.')
        )
        return redirect('users')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        if user_id == request.user.id:
            user = User.objects.get(id=user_id)
            if user:
                user.delete()
                messages.success(request, _('User successfully deleted'))
        return redirect('users')
