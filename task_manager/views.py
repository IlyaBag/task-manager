from typing import Any

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _


def index(request):
    """Render the index page."""
    return render(request, 'index.html')


class UserLoginView(LoginView):
    """Add a success flash message to a parent class"""

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        messages.success(self.request, _('You are logged in'))
        return HttpResponseRedirect(self.get_success_url())


class UserLogoutView(LogoutView):
    """Add a success flash message to a parent class"""

    def post(self,
             request: WSGIRequest,
             *args: Any,
             **kwargs: Any) -> TemplateResponse:
        messages.info(request, _('You are logged out'))
        return super().post(request, *args, **kwargs)
