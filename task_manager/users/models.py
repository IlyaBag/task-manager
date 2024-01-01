from django.contrib.auth.models import User


User.add_to_class("__str__", User.get_full_name)
