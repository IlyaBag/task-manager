from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    """Customized form for creating a new user."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class UserUpdateForm(UserCreateForm):
    """
    A form for updating user info whithout checking the 'username' field for
    uniqueness.
    """

    def clean_username(self):
        return self.cleaned_data.get("username")
