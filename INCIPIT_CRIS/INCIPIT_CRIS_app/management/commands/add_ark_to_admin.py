from django.core.management.base import BaseCommand, CommandError
from os.path import isfile, join
from django.conf import settings
import requests
from INCIPIT_CRIS_app.models import User


class Command(BaseCommand):
    help = 'Add an artificial ARK to the admin count to be refenrenced and editable'

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.get(username='admin')
            print(user)
            user.pid = 'ark:/00000/0'
            print(user.pid)
            user.clean()
            print(user)
            user.save()
        except Exception as e:
            print(e)
            raise CommandError('Initalization failed.')