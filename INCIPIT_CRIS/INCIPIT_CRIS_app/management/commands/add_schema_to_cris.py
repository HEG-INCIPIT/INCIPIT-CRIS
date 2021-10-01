from django.core.management.base import BaseCommand, CommandError
from os.path import isfile, join
from django.conf import settings
import requests

class Command(BaseCommand):
    help = 'Add the schema ontology to the triplestore'

    def handle(self, *args, **kwargs):
        try:
            if isfile(join(settings.SCHEMA_ROOT, settings.SCHEMA_FILE_NAME)):
                f = open(join(settings.SCHEMA_ROOT, settings.SCHEMA_FILE_NAME), 'r')
                data = f.read()
                f.close()
                headers = {'Content-Type': 'text/turtle;charset=utf-8'}
                r = requests.post('http://localhost:3030/INCIPIT-CRIS/data?default', auth=(settings.FUSEKI_USER, settings.FUSEKI_PASSWORD), data=data.encode('utf-8'), headers=headers)
                if r.status_code == 200:
                    print('Succesfull')
            else:
                print('File not found')
        except:
            raise CommandError('Initalization failed.')