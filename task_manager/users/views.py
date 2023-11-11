# from django.shortcuts import render
from typing import Any
from django.views.generic.base import TemplateView

from task_manager.users.models import User


# def index(request):
#     return render(request, 'users-list.html')

class UsersView(TemplateView):
    template_name = 'users-list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context
    