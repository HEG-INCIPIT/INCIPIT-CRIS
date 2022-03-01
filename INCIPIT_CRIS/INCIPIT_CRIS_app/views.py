from logging import raiseExceptions
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
import csv
from django.contrib.auth import get_user_model


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
                accepted_format_dictionnary = ['ttl', 'n3', 'nt', 'rdf', 'owl', 'nq', 'trig', 'jsonld', 'csv', 'txt']
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
            pid_exists = ''
            if 'pid_exists' in request.session:
                pid_exists = request.session['pid_exists']
                request.session['pid_exists'] = ''
            media_path = settings.MEDIA_ROOT
            triple_files = []
            csv_files = []
            if path.isdir(media_path):
                for f in listdir(media_path):
                    if isfile(join(media_path, f)):
                        if os.path.splitext(f)[1] in [".csv", ".txt"]:
                            csv_files.append(f)
                        else:
                            triple_files.append(f)

                #my_files = [f for f in listdir(media_path) if isfile(join(media_path, f))]
                triple_files.sort(key=lambda x: os.path.getmtime('{}/{}'.format(media_path, x)), reverse=True)
                csv_files.sort(key=lambda x: os.path.getmtime('{}/{}'.format(media_path, x)), reverse=True)

            return render(request, 'data/manage_data.html', {'triple_files': triple_files, 'csv_files': csv_files, 'pid_exists': pid_exists})


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


def add_data_from_csv(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                media_path = settings.MEDIA_ROOT
                if isfile(join(media_path, request.POST['filename'])):
                    if request.POST['filename'].split('.')[-1].lower() in ['csv', 'txt']:
                        # Write data of the file in two variables
                        file = open(path.join(settings.MEDIA_ROOT, request.POST['filename']))
                        csvreader = csv.reader(file)
                        header = []
                        header = next(csvreader)
                        header = [h.lower() for h in header]
                        rows = []
                        for row in csvreader:
                            if len(row) != len(header):
                                raise ValueError('Length : header row, are not the same')
                            rows.append(row)
                        file.close()
                        # print(header)
                        # print(rows)
                        if 'article' in request.POST['filename'].lower():
                            fields_to_check = ['abstract','ark','url','datepublished','authorsark','projectsark','datasetsark','institutionsark', 'doi']
                            # Check if the header contain at least the name of the articles (it's mandatory)
                            if not('name' in header):
                                raise ValueError("The header doesn't contain minimum field : 'name'")
                            dict_header = {}
                            # Check if fields of the header are well formed
                            for i,h in enumerate(header):
                                if not(h in fields_to_check) and not(h == 'name'):
                                    raise ValueError('The header is badly formed')
                                # Add to dictionary index of element of the header
                                dict_header[h] = i

                            # Iterate over the rows of the file
                            for row in rows:
                                if row[dict_header['name']] == '':
                                    raise ValueError('No name found for article')
                                pid = row[dict_header['ark']] if 'ark' in dict_header.keys() else ''
                                if pid == '':
                                    try:
                                        pid = variables.ark.mint(row[dict_header['url']] if 'url' in dict_header.keys() else '', 'Admin',
                                            row[dict_header['name']], row[dict_header['datepublished']] if 'datepublished' in dict_header.keys() else '')
                                    except:
                                        raise Exception

                                # Add data to triplestore
                                variables.sparql_post_article_object.create_article(pid, row[dict_header['name']], row[dict_header['abstract']] if 'abstract' in dict_header.keys() else '',
                                    row[dict_header['datepublished']] if 'datepublished' in dict_header.keys() else '', row[dict_header['url']] if 'url' in dict_header.keys() else '')

                                if 'authorsark' in dict_header.keys() and row[dict_header['authorsark']] != '':
                                    authorsark = row[dict_header['authorsark']].split()
                                    for author in authorsark:
                                        variables.sparql_post_article_object.add_author_to_article(pid, author)
                                
                                if 'projectsark' in dict_header.keys() and row[dict_header['projectsark']] != '':
                                    projectsark = row[dict_header['projectsark']].split()
                                    for project in projectsark:
                                        variables.sparql_post_article_object.add_project_to_article(pid, project)

                                if 'datasetsark' in dict_header.keys() and row[dict_header['datasetsark']] != '':
                                    datasetsark = row[dict_header['datasetsark']].split()
                                    for dataset in datasetsark:
                                        variables.sparql_post_article_object.add_dataset_to_article(pid, dataset)
                                
                                if 'institutionsark' in dict_header.keys() and row[dict_header['institutionsark']] != '':
                                    institutionsark = row[dict_header['institutionsark']].split()
                                    for institution in institutionsark:
                                        variables.sparql_post_article_object.add_institution_to_article(pid, institution)

                                if 'doi' in dict_header.keys() and row[dict_header['doi']] != '':
                                    variables.sparql_post_article_object.add_DOI_article(pid, row[dict_header['doi']])

                        elif 'project' in request.POST['filename'].lower():
                            fields_to_check = ['description','ark','url','urllogo','foundingdate','dissolutiondate','membersark','articlesark','datasetsark','institutionsark', 'fundersark']
                            # Check if the header contain at least the name of the projects (it's mandatory)
                            if not('name' in header):
                                raise ValueError("The header doesn't contain minimum field : 'name'")
                            dict_header = {}
                            # Check if fields of the header are well formed
                            for i,h in enumerate(header):
                                if not(h in fields_to_check) and not(h == 'name'):
                                    raise ValueError('The header is badly formed')
                                # Add to dictionary index of element of the header
                                dict_header[h] = i

                            # Iterate over the rows of the file
                            for row in rows:
                                if row[dict_header['name']] == '':
                                    raise ValueError('No name found for project')
                                pid = row[dict_header['ark']] if 'ark' in dict_header.keys() else ''
                                if pid == '':
                                    try:
                                        pid = variables.ark.mint(row[dict_header['url']] if 'url' in dict_header.keys() else '', 'Admin',
                                            row[dict_header['name']], row[dict_header['foundingdate']] if 'foundingdate' in dict_header.keys() else '')
                                    except:
                                        raise Exception

                                # Add data to triplestore
                                variables.sparql_post_project_object.create_project(pid, row[dict_header['name']], row[dict_header['description']] if 'description' in dict_header.keys() else '',
                                    row[dict_header['foundingdate']] if 'foundingdate' in dict_header.keys() else '', row[dict_header['dissolutionDate']] if 'dissolutionDate' in dict_header.keys() else '',
                                    row[dict_header['url']] if 'url' in dict_header.keys() else '', row[dict_header['urllogo']] if 'urllogo' in dict_header.keys() else '')

                                if 'membersark' in dict_header.keys() and row[dict_header['membersark']] != '':
                                    membersark = row[dict_header['membersark']].split()
                                    for member in membersark:
                                        variables.sparql_post_project_object.add_member_to_project(pid, member)
                                
                                if 'articlesark' in dict_header.keys() and row[dict_header['articlesark']] != '':
                                    articlesark = row[dict_header['articlesark']].split()
                                    for article in articlesark:
                                        variables.sparql_post_project_object.add_article_to_project(pid, article)

                                if 'datasetsark' in dict_header.keys() and row[dict_header['datasetsark']] != '':
                                    datasetsark = row[dict_header['datasetsark']].split()
                                    for dataset in datasetsark:
                                        variables.sparql_post_project_object.add_dataset_to_project(pid, dataset)
                                
                                if 'institutionsark' in dict_header.keys() and row[dict_header['institutionsark']] != '':
                                    institutionsark = row[dict_header['institutionsark']].split()
                                    for institution in institutionsark:
                                        variables.sparql_post_project_object.add_institution_to_project(pid, institution)

                                if 'fundersark' in dict_header.keys() and row[dict_header['fundersark']] != '':
                                    fundersark = row[dict_header['fundersark']].split()
                                    for funder in fundersark:
                                        variables.sparql_post_project_object.add_funder_to_project(pid, funder)
                        
                        elif 'dataset' in request.POST['filename'].lower():
                            fields_to_check = ['abstract','ark','urldetails','urldata','datecreated','datemodified','creatorsark','maintainersark','articlesark','projectsark','institutionsark']
                            # Check if the header contain at least the name of the dataset (it's mandatory)
                            if not('name' in header):
                                raise ValueError("The header doesn't contain minimum field : 'name'")
                            dict_header = {}
                            # Check if fields of the header are well formed
                            for i,h in enumerate(header):
                                if not(h in fields_to_check) and not(h == 'name'):
                                    raise ValueError('The header is badly formed')
                                # Add to dictionary index of element of the header
                                dict_header[h] = i

                            # Iterate over the rows of the file
                            for row in rows:
                                if row[dict_header['name']] == '':
                                    raise ValueError('No name found for dataset')
                                pid = row[dict_header['ark']] if 'ark' in dict_header.keys() else ''
                                if pid == '':
                                    try:
                                        pid = variables.ark.mint(row[dict_header['urldata']] if 'urldata' in dict_header.keys() else '', 'Admin',
                                            row[dict_header['name']], row[dict_header['datecreated']] if 'datecreated' in dict_header.keys() else '')
                                    except:
                                        raise Exception

                                # Add data to triplestore
                                variables.sparql_post_dataset_object.create_dataset(pid, row[dict_header['name']], row[dict_header['abstract']] if 'abstract' in dict_header.keys() else '',
                                    row[dict_header['datecreated']] if 'datecreated' in dict_header.keys() else '', row[dict_header['datemodified']] if 'datemodified' in dict_header.keys() else '',
                                    row[dict_header['urldata']] if 'urldata' in dict_header.keys() else '', row[dict_header['urldetails']] if 'urldetails' in dict_header.keys() else '')

                                if 'creatorsark' in dict_header.keys() and row[dict_header['creatorsark']] != '':
                                    creatorsark = row[dict_header['creatorsark']].split()
                                    for creator in creatorsark:
                                        variables.sparql_post_dataset_object.add_creator_to_dataset(pid, creator)
                                
                                if 'maintainersark' in dict_header.keys() and row[dict_header['maintainersark']] != '':
                                    maintainersark = row[dict_header['maintainersark']].split()
                                    for maintainer in maintainersark:
                                        variables.sparql_post_dataset_object.add_maintainer_to_dataset(pid, maintainer)

                                if 'articlesark' in dict_header.keys() and row[dict_header['articlesark']] != '':
                                    articlesark = row[dict_header['articlesark']].split()
                                    for article in articlesark:
                                        variables.sparql_post_dataset_object.add_article_to_dataset(pid, article)
                                    
                                if 'projectsark' in dict_header.keys() and row[dict_header['projectsark']] != '':
                                    projectsark = row[dict_header['projectsark']].split()
                                    for project in projectsark:
                                        variables.sparql_post_dataset_object.add_project_to_dataset(pid, project)
                                
                                if 'institutionsark' in dict_header.keys() and row[dict_header['institutionsark']] != '':
                                    institutionsark = row[dict_header['institutionsark']].split()
                                    for institution in institutionsark:
                                        variables.sparql_post_dataset_object.add_institution_to_dataset(pid, institution)

                        elif 'institution' in request.POST['filename'].lower():
                            fields_to_check = ['alternatename','description','ark','url','urllogo','foundingdate','parentorganizationsark','suborganizationsark','workersark','affiliatesark','articlesark','projectsark','datasetsark','funder']
                            # Check if the header contain at least the name of the institution (it's mandatory)
                            if not('name' in header):
                                raise ValueError("The header doesn't contain minimum field : 'name'")
                            dict_header = {}
                            # Check if fields of the header are well formed
                            for i,h in enumerate(header):
                                if not(h in fields_to_check) and not(h == 'name'):
                                    raise ValueError('The header is badly formed')
                                # Add to dictionary index of element of the header
                                dict_header[h] = i
                            
                            # Iterate over the rows of the file
                            for row in rows:
                                if row[dict_header['name']] == '':
                                    raise ValueError('No name found for dataset')
                                pid = row[dict_header['ark']] if 'ark' in dict_header.keys() else ''
                                if pid == '':
                                    try:
                                        pid = variables.ark.mint(row[dict_header['url']] if 'url' in dict_header.keys() else '', 'Admin',
                                            row[dict_header['name']], row[dict_header['foundingdate']] if 'foundingdate' in dict_header.keys() else '')
                                    except:
                                        raise Exception

                                # Add data to triplestore
                                variables.sparql_post_institution_object.create_institution(pid, row[dict_header['name']], row[dict_header['alternatename']] if 'alternatename' in dict_header.keys() else '',
                                    row[dict_header['description']] if 'description' in dict_header.keys() else '',
                                    row[dict_header['foundingdate']] if 'foundingdate' in dict_header.keys() else '', row[dict_header['url']] if 'url' in dict_header.keys() else '',
                                    row[dict_header['urllogo']] if 'urllogo' in dict_header.keys() else '', '')

                                if 'parentorganizationsark' in dict_header.keys() and row[dict_header['parentorganizationsark']] != '':
                                    parentorganizationsark = row[dict_header['parentorganizationsark']].split()
                                    for parent_organization in parentorganizationsark:
                                        variables.sparql_post_institution_object.add_parent_institution_to_institution(pid, parent_organization)
                                
                                if 'suborganizationsark' in dict_header.keys() and row[dict_header['suborganizationsark']] != '':
                                    suborganizationsark = row[dict_header['suborganizationsark']].split()
                                    for sub_organization in suborganizationsark:
                                        variables.sparql_post_institution_object.add_sub_institution_to_institution(pid, sub_organization)

                                if 'workersark' in dict_header.keys() and row[dict_header['workersark']] != '':
                                    workersark = row[dict_header['workersark']].split()
                                    for worker in workersark:
                                        variables.sparql_post_institution_object.add_worker_to_institution(pid, worker)
                                    
                                if 'projectsark' in dict_header.keys() and row[dict_header['projectsark']] != '':
                                    projectsark = row[dict_header['projectsark']].split()
                                    for project in projectsark:
                                        variables.sparql_post_dataset_object.add_project_to_dataset(pid, project)
                                
                                if 'affiliatesark' in dict_header.keys() and row[dict_header['affiliatesark']] != '':
                                    affiliatesark = row[dict_header['affiliatesark']].split()
                                    for affiliate in affiliatesark:
                                        variables.sparql_post_institution_object.add_affiliate_to_institution(pid, affiliate)
                                
                                if 'articlesark' in dict_header.keys() and row[dict_header['articlesark']] != '':
                                    articlesark = row[dict_header['articlesark']].split()
                                    for article in articlesark:
                                        variables.sparql_post_institution_object.add_article_to_institution(pid, article)

                                if 'projectsark' in dict_header.keys() and row[dict_header['projectsark']] != '':
                                    projectsark = row[dict_header['projectsark']].split()
                                    for project in projectsark:
                                        variables.sparql_post_institution_object.add_project_to_institution(pid, project)

                                if 'datasetsark' in dict_header.keys() and row[dict_header['datasetsark']] != '':
                                    datasetsark = row[dict_header['datasetsark']].split()
                                    for dataset in datasetsark:
                                        variables.sparql_post_institution_object.add_dataset_to_institution(pid, dataset)

                                if 'funder' in dict_header.keys() and row[dict_header['funder']] != '' and row[dict_header['funder']] == 'True':
                                    variables.sparql_post_funder_object.define_institution_funder(pid)

                        elif 'person' in request.POST['filename'].lower():
                            pid_exists = []
                            fields_to_check = ['email','firstname','lastname','ark']
                            # Check if the header contain at least the name of the institution (it's mandatory)
                            if not('username' in header):
                                raise ValueError("The header doesn't contain minimum field : 'username'")
                            dict_header = {}
                            # Check if fields of the header are well formed
                            for i,h in enumerate(header):
                                if not(h in fields_to_check) and not(h == 'username'):
                                    raise ValueError('The header is badly formed')
                                # Add to dictionary index of element of the header
                                dict_header[h] = i

                             # Iterate over the rows of the file
                            for row in rows:
                                if row[dict_header['username']] == '':
                                    raise ValueError('No name found for dataset')
                                pid = row[dict_header['ark']] if 'ark' in dict_header.keys() else ''
                                if pid == '':
                                    try:
                                        pid = variables.ark.mint('', 'Admin',
                                            'An ARK created in INCIPIT-CRIS for a person named {} {}'.format(row[dict_header['firstname']], row[dict_header['lastname']]), datetime.datetime.now())
                                        variables.ark.update('{}'.format(pid), '{}{}'.format(settings.URL, pid), 'Admin',
                                            'An ARK created in INCIPIT-CRIS for a person named {} {}'.format(row[dict_header['firstname']], row[dict_header['lastname']]), datetime.datetime.now())
                                    except:
                                        raise Exception

                                User = get_user_model()
                                if User.objects.filter(pid=pid).exists():
                                    print(pid)
                                    pid_exists.append(pid)
                                else:
                                    user = User.objects.create_user(username=row[dict_header['username']], email=row[dict_header['email']], first_name=row[dict_header['firstname']], last_name=row[dict_header['lastname']], pid=pid)
                                    user.is_active = False
                                    user.save()
                                if len(pid_exists) > 0:
                                    request.session['pid_exists'] = pid_exists
    
    return redirect(manage_data)


def delete_data(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            media_path = settings.MEDIA_ROOT
            if isfile(join(media_path, request.POST['filename'])):
                remove(path.join(settings.MEDIA_ROOT, request.POST['filename']))

            return redirect(manage_data)
