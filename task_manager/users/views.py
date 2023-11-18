from typing import Any

# from django.shortcuts import render
# from django.views import View
# from django import http
# from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView


class UsersView(TemplateView):
    template_name = 'users-list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


# # def index(request):
# #     return render(request, 'users-list.html')

# class UsersView(TemplateView):
#     template_name = 'users-list.html'

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context['users'] = User.objects.all()
#         return context
    
# class UserFormCreateView(View):

#     def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
#         form = UserForm()
#         return render(request, 'user-create.html', {'form': form})
#     # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
#     #     return super().get(request, *args, **kwargs)
