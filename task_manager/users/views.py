from typing import Any

# from django.shortcuts import render
# from django.views import View
# from django.http import HttpRequest, HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from .forms import UserCreateForm


class UsersView(TemplateView):
    template_name = 'users/users-list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class UserCreateView(CreateView):
    template_name = 'users/user-create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('users')  # 'login'


# class UserFormCreateView(View):

#     def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
#         form = UserForm()
#         return render(request, 'user-create.html', {'form': form})
#     # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
#     #     return super().get(request, *args, **kwargs)
