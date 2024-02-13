import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from dotenv import load_dotenv


load_dotenv()

SU_PASSWORD = os.getenv('SU_PASSWORD')


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username=options.get('username', 'admin'),
                password=SU_PASSWORD,
            )
