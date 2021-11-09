import string
import re
import json
import os
import requests
from .forms import URLForm
from .models import User
from django.shortcuts import render, redirect
from .forms import *
from .views import index
from . import variables
from . import form_selection
from INCIPIT_CRIS_app.models import Title, JobTitle


def person_results(request):
    '''
    Search in the triplestore all the persons and format a dictionnary that's used
    in the template to display information.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display results for persons and a dictionnary with all the data needed to fulfill
        the template.
    '''

    alphabet_list = list(string.ascii_lowercase)
    categories = ['Personnes']
    category = categories[0]
    sparql_request = variables.sparql_get_person_object.get_persons()
    context = {
        'path_name' : ['Personnes'],
        'path_url' : ['/persons/'],
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
    }

    return render(request, 'person/person_results.html', context)


def person_profile(request, pid):
    '''
    Display a page with all the data of a person that is given by the pid.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the profil of a person and a dictionnary with all the data needed to fulfill
        the template.
    '''

    context = {}
    can_edit = True if request.user.is_authenticated and (request.user.pid == pid or request.user.is_superuser) else False
    
    # Verify in triplestore if the pid correspond to a person
    if variables.sparql_get_person_object.check_person_ark(pid):

        data_person = variables.sparql_get_person_object.get_data_person(pid)

        '''
        Some elements contained in the dictionnary data_person :
        
        data_person['articles'] : all data of articles for whom the person is author
        data_person['projects'] : all data of projects for whom the person is member
        data_person['pid'] : ark pid of the person
        '''

        context = {
            'data_person': data_person,
            'can_edit': can_edit,
        }
        return render(request, 'person/person_profile.html', context)

    return render(request, 'page_404.html')


def person_edition(request, pid):
    '''
    Display a page with all the data of the person given by the pid and adds links to modify some parts.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the profil of a person with the fields that can be edited and a dictionnary
        with all the data needed to fulfill the template.
    '''

    # Verify in triplestore if the pid correspond to a person
    if variables.sparql_get_person_object.check_person_ark(pid):
        context = {}
        if request.user.is_authenticated and (request.user.pid == pid or request.user.is_superuser):
            data_person = variables.sparql_get_person_object.get_data_person(pid)
            try:
                context = {
                    'data_person': data_person,
                    'url_auth': os.environ['url_auth']
                }
            except:
                context = {
                    'data_person': data_person,
                    'url_auth': ''
                }
            return render(request, 'person/person_profile_edition.html', context)
        else:
            if request.user.is_authenticated:
                context = {
                    'message': "Vous n'avez pas le droit d'éditer ce profil"
                }
            else:
                context = {
                    'message': "Connectez-vous pour modifier votre profil"
                }
        return render(request, 'page_info.html', context)

    return render(request, 'page_404.html')


def person_field_edition(request, field_to_modify, pid):
    '''
    Handle the display and the selection of the correct form to modify a given field

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    field_to_modify : String
        Indicates the field that is asked to be modified.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the field of the profil of a person that is going to be modified and a dictionnary
        with all the data needed to fulfill the template.
    '''
    context = {}
    form = forms.Form()
    # Verify in triplestore if the pid correspond to a person
    if variables.sparql_get_person_object.check_person_ark(pid):
        # Verify that the user is authenticated and has the right to modify the profile
        if request.user.is_authenticated and (request.user.pid == pid or request.user.is_superuser):
            data_person = variables.sparql_get_person_object.get_data_person(pid)
            form = form_selection.form_selection(request, field_to_modify, data_person)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    variables.sparql_generic_post_object.update_string_leaf(pid, field_to_modify,
                                                                  form.cleaned_data[field_to_modify],
                                                                  data_person[field_to_modify])
                    return redirect(person_edition, pid=pid)
                
                return render(request, 'page_error.html')

            context = {
                'form': form,
                'path_name' : ['Personnes', 'Profil', 'Edition', form.fields[next(iter(form.declared_fields.keys()))].label],
                'path_url' : ['/persons/', '/persons/'+pid, '/persons/edition/'+pid, '/persons/edition/profil/'+field_to_modify+pid],
                'button_value': 'Modifier',
                'url_to_return': '/persons/edition/profil/{}/{}'.format(field_to_modify, pid)
            }
            return render(request, 'forms/classic_form.html', context)

        # Check why the person cannot modify the profile and display the error
        if request.user.is_authenticated:
            context = {
                'message': "Vous n'avez pas le droit d'éditer ce profil"
            }
        else:
            context = {
                'message': "Connectez-vous pour modifier ce profil"
            }
        
        return render(request, 'page_info.html', context)

    return render(request, 'page_404.html')


def person_article_deletion(request, pid):
    '''
    Deletes an article of a given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:
            article = request.POST.get('articleARK', '')
            variables.sparql_post_article_object.delete_author_of_article(article, pid)

            return redirect(person_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def person_article_addition(request, pid):
    '''
    Adds an article to a given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    context = {}
    
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify if the user as the right to modify the profile
        if request.user.is_superuser:
            
            # Check the request method
            if request.method == 'POST':
                articles = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for article in articles:
                    variables.sparql_post_article_object.add_author_to_article(article.split()[-1], pid)

                return redirect(person_edition, pid=pid)

            articles = []
            # Request all the articles in the triplestore
            articles_info = variables.sparql_get_article_object.get_articles()
            # Request all the articles of the person
            articles_person = variables.sparql_get_person_object.get_articles_person(pid)
            for basic_info_article in articles_info:
                if not (basic_info_article[0] in [article['pid'] for article in articles_person]):
                    articles.append(
                        '''{}, {}'''.format(basic_info_article[1], basic_info_article[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Personnes', 'Profil', 'Edition', 'Ajouter un article'],
                'path_url' : ['/persons/', '/persons/'+pid, '/persons/edition/'+pid, '/persons/edition/profil/add-article/'+pid],
                'title_data_type_added': 'Article',
                'data_type_added': 'de l\'article',
                'url_to_return': '/persons/edition/profil/add-article/{}'.format(pid),
                'data': articles
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cette personne",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cette personne"
    }
    return render(request, 'page_info.html', context)


def person_project_addition(request, pid):
    '''
    Adds a project to a given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify if the user as the right to modify the profile
        if request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                projects = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for project in projects:
                    variables.sparql_post_project_object.add_member_to_project(project.split()[-1], pid)

                return redirect(person_edition, pid=pid)

            projects = []
            # Request all the projects in the triplestore
            projects_info = variables.sparql_get_project_object.get_projects()
            # Request all the projects of the person
            projects_person = variables.sparql_get_person_object.get_projects_person(pid)
            for basic_info_project in projects_info:
                if not (basic_info_project[0] in [project['pid'] for project in projects_person]):
                    projects.append(
                        '''{}, {}'''.format(basic_info_project[1], basic_info_project[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Personnes', 'Profil', 'Edition', 'Ajouter un projet'],
                'path_url' : ['/persons/', '/persons/'+pid, '/persons/edition/'+pid, '/persons/edition/profil/add-project/'+pid],
                'title_data_type_added': 'Projet',
                'data_type_added': 'du projet',
                'url_to_return': '/persons/edition/profil/add-project/{}'.format(pid),
                'data': projects
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_project_deletion(request, pid):
    '''
    Deletes a project of the given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:
            project = request.POST.get('projectARK', '')
            variables.sparql_post_project_object.delete_member_of_project(project, pid)

            return redirect(person_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_datasets_addition(request, pid):
    '''
    Adds a dataset as creator to a given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify if the user as the right to modify the profile
        if request.user.is_superuser:
            # Check the request method
            if request.method == 'POST':
                datasets = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                person_status = request.POST['personStatus']
                if person_status == 'creator':
                    for dataset in datasets:
                        variables.sparql_post_dataset_object.add_creator_to_dataset(dataset.split()[-1], pid)
                elif person_status == 'maintainer':
                    for dataset in datasets:
                        variables.sparql_post_dataset_object.add_maintainer_to_dataset(dataset.split()[-1], pid)
                elif person_status == 'creator_and_maintainer':
                    for dataset in datasets:
                        variables.sparql_post_dataset_object.add_creator_to_dataset(dataset.split()[-1], pid)
                        variables.sparql_post_dataset_object.add_maintainer_to_dataset(dataset.split()[-1], pid)

                return redirect(person_edition, pid=pid)

            datasets = []
            # Request all the datasets in the triplestore
            datasets_info = variables.sparql_get_dataset_object.get_datasets()
            # Request all the datasets of the person
            datasets_person = variables.sparql_get_person_object.get_datasets_creator_person(pid)
            for basic_info_dataset in datasets_info:
                if not (basic_info_dataset[0] in [dataset['pid'] for dataset in datasets_person]):
                    datasets.append(
                        '''{}, {}'''.format(basic_info_dataset[1], basic_info_dataset[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Personnes', 'Profil', 'Edition', 'Ajouter un jeu de données'],
                'path_url' : ['/persons/', '/persons/'+pid, '/persons/edition/'+pid, '/persons/edition/profil/add-dataset/'+pid],
                'title_data_type_added': 'Jeu de données',
                'data_type_added': 'du jeu de données',
                'url_to_return': '/persons/edition/profil/add-dataset/{}'.format(pid),
                'data': datasets
            }
            # return the form to be completed
            return render(request, 'forms/person_dataset_addition.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_datasets_deletion(request, pid):
    '''
    Deletes a dataset of a given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            dataset = request.POST.get('dataset_ARK', '')
            variables.sparql_post_dataset_object.delete_creator_of_dataset(dataset, pid)
            variables.sparql_post_dataset_object.delete_maintainer_of_dataset(dataset, pid)

            return redirect(person_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_datasets_maintainer_addition(request, pid):
    '''
    Adds a dataset as maintainer to a given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify if the user as the right to modify the profile
        if request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                datasets = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for dataset in datasets:
                    variables.sparql_post_dataset_object.add_maintainer_to_dataset(dataset.split()[-1], pid)

                return redirect(person_edition, pid=pid)

            datasets = []
            # Request all the datasets in the triplestore
            datasets_info = variables.sparql_get_dataset_object.get_datasets()
            # Request all the datasets of the person
            datasets_person = variables.sparql_get_person_object.get_datasets_maintainer_person(pid)
            for basic_info_dataset in datasets_info:
                if not (basic_info_dataset[0] in [dataset[0] for dataset in datasets_person]):
                    datasets.append(
                        '''{}, {}'''.format(basic_info_dataset[1], basic_info_dataset[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Personnes', 'Profil', 'Edition', 'Ajouter un jeu de données en tant que mainteneur'],
                'path_url' : ['/persons/', '/persons/'+pid, '/persons/edition/'+pid, '/persons/edition/profil/add-maintainer/'+pid],
                'title_data_type_added': 'Jeu de données',
                'data_type_added': 'du jeu de données',
                'url_to_return': '/persons/edition/profil/add-dataset-maintainer/{}'.format(pid),
                'data': datasets
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_work_addition(request, pid):
    '''
    Adds an organisation where the given person works

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                organization = request.POST['institutions']
                if organization != '':
                    variables.sparql_post_person_object.add_work_person(pid, organization)
                elif organization == '':
                    variables.sparql_post_person_object.delete_work_person(pid, organization)

                return redirect(person_edition, pid=pid)

            top_lvl_institutions = variables.sparql_get_institution_object.get_top_lvl_institutions()
            top_lvl_institutions_data = []
            for top_lvl_institution in top_lvl_institutions:
                top_lvl_institutions_data.append(variables.sparql_get_institution_object.get_dict_institution(top_lvl_institution[0]))

            context = {
                'path_name' : ['Personnes', 'Profil', 'Edition', 'Ajouter une institution de travail'],
                'path_url' : ['/persons/', '/persons/'+pid, '/persons/edition/'+pid, '/persons/edition/profil/add-work/'+pid],
                'title_data_type_added': 'Institution de travail',
                'data_type_added': 'de l\'institution de travail',
                'url_to_return': '/persons/edition/profil/add-work/{}'.format(pid),
                'button_value': 'Ajouter',
                'institutions': json.dumps(top_lvl_institutions_data),
            }

            return render(request, 'forms/select_institution_form.html', context)
    
        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_work_deletion(request, pid):
    '''
    Edit an organisation where the given person works

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Get the value of a variable in the POST request by its id
            work = request.POST.get('workARK', '')
            variables.sparql_post_person_object.delete_work_person(pid, work)

            return redirect(person_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_affiliation_addition(request, pid):
    '''
    Adds an organisation where the given person affiliations

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                organization = request.POST['institutions']
                if organization != '':
                    variables.sparql_post_person_object.add_affiliation_person(pid, organization)
                elif organization == '':
                    variables.sparql_post_person_object.delete_affiliation_person(pid, organization)

                return redirect(person_edition, pid=pid)

            top_lvl_institutions = variables.sparql_get_institution_object.get_top_lvl_institutions()
            top_lvl_institutions_data = []
            for top_lvl_institution in top_lvl_institutions:
                top_lvl_institutions_data.append(variables.sparql_get_institution_object.get_dict_institution(top_lvl_institution[0]))

            context = {
                'path_name' : ['Personnes', 'Profil', 'Edition', 'Ajouter une institution de travail'],
                'path_url' : ['/persons/', '/persons/'+pid, '/persons/edition/'+pid, '/persons/edition/profil/add-affiliation/'+pid],
                'title_data_type_added': 'Institution de travail',
                'data_type_added': 'de l\'institution de travail',
                'url_to_return': '/persons/edition/profil/add-affiliation/{}'.format(pid),
                'button_value': 'Ajouter',
                'institutions': json.dumps(top_lvl_institutions_data),
            }

            return render(request, 'forms/select_institution_form.html', context)
    
        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_affiliation_deletion(request, pid):
    '''
    Edit an organisation where the given person affiliations

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Get the value of a variable in the POST request by its id
            affiliation = request.POST.get('affiliationARK', '')
            variables.sparql_post_person_object.delete_affiliation_person(pid, affiliation)

            return redirect(person_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_title_addition(request, pid):
    '''
    Adds an title where the given person works

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                title = request.POST['select-data']
                if title != '':
                    variables.sparql_post_person_object.add_title_person(pid, title)

                return redirect(person_edition, pid=pid)

            titles = list(Title.objects.order_by('title').values_list('title', flat=True))

            context = {
                'path_name' : ['Personnes', 'Profil', 'Edition', 'Ajouter un titre'],
                'path_url' : ['/persons/', '/persons/'+pid, '/persons/edition/'+pid, '/persons/edition/profile/add-title/'+pid],
                'title_data_type_added': 'Ajouter un titre',
                'data_type_added': 'Titre',
                'url_to_return': '/persons/edition/profil/add-title/{}'.format(pid),
                'button_value': 'Ajouter',
                'data': titles,
            }

            return render(request, 'forms/select_form_from_array.html', context)
    
        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_title_deletion(request, pid):
    '''
    Delete the title of a given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Get the value of a variable in the POST request by its id
            title = request.POST['title']
            variables.sparql_post_person_object.delete_title_person(pid, title)

            return redirect(person_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }


def person_job_title_addition(request, pid):
    '''
    Adds an job_title where the given person works

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                job_title = request.POST['select-data']
                if job_title != '':
                    variables.sparql_post_person_object.add_job_title_person(pid, job_title)

                return redirect(person_edition, pid=pid)

            job_titles = list(JobTitle.objects.order_by('job_title').values_list('job_title', flat=True))

            context = {
                'path_name' : ['Personnes', 'Profil', 'Edition', 'Ajouter un titre'],
                'path_url' : ['/persons/', '/persons/'+pid, '/persons/edition/'+pid, '/persons/edition/profile/add-job-title/'+pid],
                'title_data_type_added': 'Ajouter un poste de travail',
                'data_type_added': 'Poste de travail',
                'url_to_return': '/persons/edition/profil/add-job-title/{}'.format(pid),
                'button_value': 'Ajouter',
                'data': job_titles,
            }

            return render(request, 'forms/select_form_from_array.html', context)
    
        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_job_title_deletion(request, pid):
    '''
    Delete the job_title of a given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Get the value of a variable in the POST request by its id
            job_title = request.POST['job_title']
            variables.sparql_post_person_object.delete_job_title_person(pid, job_title)

            return redirect(person_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def orcid(request):

    if not request.user.is_superuser:
    
        code = request.GET.get('code', '')

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Charset': 'UTF-8'
        }

        try:
            data = {'client_id': os.environ['client_id'], 'client_secret': os.environ['client_secret'], 'grant_type': 'authorization_code', 'code': code, 'redirect_uri': os.environ['redirect_uri']}

            response = requests.post(url='https://orcid.org/oauth/token', headers=headers, data=data, allow_redirects=True, verify=False)

            if response.status_code == 200:

                user = User.objects.filter(pid=request.user.pid)
                user.update(access_token_orcid=response.json()['access_token'])
                user.update(refresh_token_orcid=response.json()['refresh_token'])
                user.update(expires_in_orcid=response.json()['expires_in'])
                user.update(orcid=response.json()['orcid'])

                data_person = variables.sparql_get_person_object.get_data_person(request.user.pid)

                variables.sparql_post_person_object.update_person_string_leaf(request.user.pid+"ORCID", "propertyID", response.json()['orcid'], data_person['orcid'])

                return redirect(person_edition, request.user.pid)
        except:

            return render(request, 'page_404.html')
    
    return redirect(index)


def delete_orcid(request, pid):
    user = User.objects.filter(pid=pid)
    user.update(access_token_orcid='')
    user.update(refresh_token_orcid='')
    user.update(expires_in_orcid='')
    user.update(orcid='')

    orcid = request.POST['orcid']

    variables.sparql_post_person_object.update_person_string_leaf(pid+"ORCID", "propertyID", '', orcid)

    return redirect(person_edition, pid)


def person_linkedin_addition(request, pid):
    '''
    Adds a linkedin url to the given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:
            data_person = variables.sparql_get_person_object.get_data_person(pid)
            # Check the request method
            if request.method == 'POST':
                form = URLForm(request.POST)
                if form.is_valid():
                    linkedin_url = form.cleaned_data['url']
                    if linkedin_url != '':
                        variables.sparql_post_person_object.add_IN_information_person(pid, linkedin_url)

                    return redirect(person_edition, pid=pid)
            
            form = URLForm(old_url=data_person['linkedin'])

            context = {
                'form': form,
                'path_name' : ['Personnes', 'Profil', 'Edition', 'Ajouter un profil LinkedIn'],
                'path_url' : ['/persons/', '/persons/'+pid, '/persons/edition/'+pid, '/persons/edition/profil/add-linkedin-profile/'+pid],
                'title_data_type_added': 'Ajouter un profil LinkedIn',
                'data_type_added': 'url du profil LinkedIn',
                'url_to_return': '/persons/edition/profil/add-linkedin-profile/{}'.format(pid),
                'button_value': 'Ajouter',
            }

            return render(request, 'forms/edited_form.html', context)
    
        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def person_linkedin_deletion(request, pid):
    '''
    Delete the linkedin url of the given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Get the value of a variable in the POST request by its id
            linkedin = request.POST.get('linkedin', '')
            variables.sparql_post_person_object.delete_IN_information_person(pid, linkedin)

            return redirect(person_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)
