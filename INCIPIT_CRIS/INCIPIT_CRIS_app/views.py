from SPARQLWrapper.Wrapper import ADD
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
import datetime
import os
from . import variables
from django.core.files.storage import FileSystemStorage
from os import listdir, remove, path
from os.path import isfile, join
from django.conf import settings
from random import sample
import requests
import mimetypes
import socket


def index(request):
    '''
    Search data of users from database, articles and project from triplestore and display it all
    in the template

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the index page and a dictionnary with all the data needed to fulfill
        the template.
    '''

    funders = variables.sparql_get_funder_object.get_funders()

    institutions = variables.sparql_get_institution_object.get_institutions()

    datasets = variables.sparql_get_dataset_object.get_datasets()

    articles = variables.sparql_get_article_object.get_articles()

    persons_triplestore = variables.sparql_get_person_object.get_persons()

    articles_data = []
    for article in articles:
        articles_data.append(variables.sparql_get_article_object.get_data_article(article[0]))
    articles_data.sort(key=lambda item: item['date_published'], reverse=True)

    # Filter users in database by their joined date
    """user_model = get_user_model()
    users = user_model.objects.all().filter(is_staff=False).order_by('date_joined')

    last_users_registered = []
    for i in range(1, min(5+1, len(users)+1)):
        last_users_registered.append([users.values('pid')[len(users) - i]['pid'],
                                      users.values('first_name')[len(users) - i]['first_name'],
                                      users.values('last_name')[len(users) - i]['last_name']])"""

    # Sample randomly but uniquely Persons
    random_persons = [persons_triplestore[i] for i in sample(range(0,len(persons_triplestore)), min(len(persons_triplestore),5))]

    projects = variables.sparql_get_project_object.get_projects()

    projects_data = []
    for project in projects:
        projects_data.append(variables.sparql_get_project_object.get_data_project(project[0]))
    projects_data.sort(key=lambda item: item['founding_date'], reverse=True)

    context = {
        'len_persons': len(persons_triplestore),
        'len_datasets': len(datasets),
        'len_institutions': len(institutions),
        'len_funders': len(funders),
        'len_articles': len(articles),
        'len_projects': len(projects_data),
        'random_persons': random_persons,
        'last_publications': articles_data[:5],
        'project_data': projects_data[:5],
        'ip': socket.gethostbyname(socket.gethostname())
    }
    return render(request, 'main/index.html', context)


def import_data(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            text_to_return = {'text': ''}
            if request.method == 'POST':
                accepted_format_dictionnary = ['ttl', 'n3', 'nt', 'rdf', 'owl', 'nq', 'trig', 'jsonld', 'csv']
                data_file = request.FILES['data_file']
                if str(data_file).split('.')[-1].lower() in accepted_format_dictionnary:
                    fs = FileSystemStorage()
                    filename = fs.save(data_file.name, data_file)
                    uploaded_file_url = fs.url(filename)
                    return render(request, 'forms/import/import_data.html', {'uploaded_file_url': uploaded_file_url})
                else:
                    text_to_return = {'text': 'Le format n\'est pas correct'}
            return render(request, 'forms/import/import_data.html', text_to_return)



def manage_data(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            media_path = settings.MEDIA_ROOT
            triple_files = []
            csv_files = []
            if path.isdir(media_path):
                for f in listdir(media_path):
                    if isfile(join(media_path, f)):
                        if os.path.splitext(f)[1] == ".csv":
                            csv_files.append(f)
                        else:
                            triple_files.append(f)

                #my_files = [f for f in listdir(media_path) if isfile(join(media_path, f))]
                triple_files.sort(key=lambda x: os.path.getmtime('{}/{}'.format(media_path, x)), reverse=True)
                csv_files.sort(key=lambda x: os.path.getmtime('{}/{}'.format(media_path, x)), reverse=True)

            return render(request, 'data/manage_data.html', {'triple_files': triple_files, 'csv_files': csv_files})


def backup_triplestore(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            backup = variables.sparql_generic_get_object.generate_backup()
            with open('{}/cris-backup-{}.ttl'.format(settings.MEDIA_ROOT, str(datetime.datetime.now())[:-7].replace(' ', '_').replace(':', '-')), 'w') as f:
                f.write(backup.decode("utf-8"))
    return redirect(manage_data)


def download_file_superuser(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if isfile(join(settings.MEDIA_ROOT, request.POST['filename'])):
                filepath = path.join(settings.MEDIA_ROOT, request.POST['filename'])
                data_file = open(filepath, 'r')
                mime_type, _ = mimetypes.guess_type(filepath)
                response = HttpResponse(data_file, content_type=mime_type)
                response['Content-Disposition'] = "attachment; filename={}".format(request.POST['filename'])
                return response

    return render(request, 'page_404.html')


def populate_triplestore(request):
    rdf_format_dictionnary = {
        'ttl': 'text/turtle;charset=utf-8',
        'n3': 'text/n3; charset=utf-8',
        'nt': 'text/plain',
        'rdf': 'application/rdf+xml',
        'owl': 'application/rdf+xml',
        'nq': 'application/n-quads',
        'trig': 'application/trig',
        'jsonld': 'application/ld+json',
    }
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                media_path = settings.MEDIA_ROOT
                if isfile(join(media_path, request.POST['filename'])):
                    extension = request.POST['filename'].split('.')[-1].lower()
                    if extension in rdf_format_dictionnary:
                        f = open(join(media_path, request.POST['filename']), 'r')
                        data = f.read()
                        f.close()
                        headers = {'Content-Type': rdf_format_dictionnary[extension]}
                        r = requests.post('http://localhost:3030/INCIPIT-CRIS/data?default', auth=(variables.sparql_variables.admin, variables.sparql_variables.password), data=data.encode('utf-8'), headers=headers)
                        print(r.status_code)

        return redirect(manage_data)


def delete_data(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            media_path = settings.MEDIA_ROOT
            if isfile(join(media_path, request.POST['filename'])):
                remove(path.join(settings.MEDIA_ROOT, request.POST['filename']))

            return redirect(manage_data)
