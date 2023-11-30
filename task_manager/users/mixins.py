from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Shows a flash message if the user is not logged in."""

    error_message = _('You are not authorized! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.error_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
