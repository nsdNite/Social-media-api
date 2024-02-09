import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management import call_command

from dotenv import load_dotenv

load_dotenv()

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            # username = username
            email = os.getenv("ADMIN_EMAIL")
            password = os.getenv("ADMIN_PASSWORD")
            print("Creating superuser")
            admin = User.objects.create_superuser(email=email, password=password)
            # admin.is_active = True
            # admin.is_admin = True
            # admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
