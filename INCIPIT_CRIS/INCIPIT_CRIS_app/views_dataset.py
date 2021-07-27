from django.shortcuts import render, redirect
from .forms import *
import re
import string
import datetime
from django.conf import settings
from . import views
from . import variables
from . import form_selection


def dataset_results(request):
    '''
    Search in the triplestore all the datasets and format a dictionnary that's used
    in the template to display information.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display results for datasets and a dictionnary with all the data needed to fulfill
        the template.
    '''
    alphabet_list = list(string.ascii_lowercase)
    categories = ['Jeux de données']
    category = categories[0]
    sparql_request = variables.sparql_get_dataset_object.get_datasets()
    context = {
        'path_name' : ['Données'],
        'path_url' : ['/datasets/'],
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
        'url':'/datasets/'
    }

    return render(request, 'generic/results.html', context)


def dataset_creation(request):
    '''
    Create in the triplestore a dataset from the data provided from the form requested

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display results for datasets and a dictionnary with all the data needed to fulfill
        the template.
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the index page.
    '''

    context = {}
    form = forms.Form()
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Check the request method
        if request.method == 'POST':
            form = DatasetCreationForm(request.POST)
            if form.is_valid():
                maintainers = re.findall('"([^"]*)"', request.POST['maintainerElementsPost'])
                creators = re.findall('"([^"]*)"', request.POST['creatorElementsPost'])
                pid = form.cleaned_data['pid']
                if pid == '':
                    try:
                        pid = variables.ark.mint(form.cleaned_data['url_data'], '{} {}'.format(request.user.first_name, request.user.first_name), 
                            form.cleaned_data['name'], form.cleaned_data['created_date'])
                    except:
                        raise Exception
                variables.sparql_post_dataset_object.create_dataset(pid, form.cleaned_data['name'],
                                                          form.cleaned_data['abstract'],
                                                          form.cleaned_data['created_date'], 
                                                          form.cleaned_data['modified_date'], 
                                                          form.cleaned_data['url_data'], 
                                                          form.cleaned_data['url_details'])
                for maintainer in maintainers:
                    variables.sparql_post_dataset_object.add_maintainer_to_dataset(pid, maintainer.split()[-1])
                for creator in creators:
                    variables.sparql_post_dataset_object.add_creator_to_dataset(pid, creator.split()[-1])
                return redirect(views.index)
        else:
            form = DatasetCreationForm()
        persons_info = variables.sparql_get_person_object.get_persons()
        persons = []
        for basic_info_person in persons_info:
            persons.append('''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))
        context = {
            'form': form,
            'button_value': 'Créer',
            'url_to_return': '/datasets/creation/',
            'persons': persons
        }
        # return the form to be completed
        return render(request, 'forms/dataset/dataset_creation.html', context)

    else:
        context = {
            'message': "Connectez-vous pour pourvoir créer des datasets"
        }

        return render(request, 'page_info.html', context)


def dataset_profile(request, pid):
    '''
    Display a page with all the data of a dataset that is given by the pid.

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
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify in triplestore if the pid correspond to a dataset
    if variables.sparql_get_dataset_object.check_dataset_ark(pid):
        # Request the data about the dataset given
        data_dataset = variables.sparql_get_dataset_object.get_data_dataset(pid)
        # Verify if the user as the rights to edit the dataset
        edition_granted = request.user.is_superuser or request.user.is_authenticated and (request.user.pid in [maintainer[0] for maintainer in data_dataset['maintainers']] or request.user.pid in [creator[0] for creator in data_dataset['creators']])
        context = {
            'edition_granted': edition_granted,
            'data_dataset': data_dataset
        }
        return render(request, 'dataset/dataset_profile.html', context)

    return render(request, 'page_404.html')


def dataset_edition(request, pid):
    '''
    Display a page with all the data of the dataset given by the pid and adds links to modify some parts.

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
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request the data of the given dataset
        data_dataset = variables.sparql_get_dataset_object.get_data_dataset(pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in data_dataset['creators']] or request.user.pid in [maintainers[0] for maintainers in data_dataset['maintainers']]:
            
            context = {
                'data_dataset': data_dataset
            }
            return render(request, 'dataset/dataset_profile_edition.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_field_edition(request, field_to_modify, pid):
    '''
    Handle the display and the selection of the correct form to modify a given field

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    part_of_article_to_modify : String
        Indicates the field that is asked to be modified.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the field of the profil of a dataset that is going to be modified and a dictionnary
        with all the data needed to fulfill the template.
    '''
    context = {}
    form = forms.Form()
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the data of the given dataset
        data_dataset = variables.sparql_get_dataset_object.get_data_dataset(pid)
        
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in data_dataset['creators']] or request.user.pid in [maintainers[0] for maintainers in data_dataset['maintainers']]:

            form = form_selection.form_selection(request, field_to_modify, data_dataset)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    if field_to_modify == 'dateCreated':
                        variables.sparql_generic_post_object.update_date_leaf(pid, field_to_modify,
                                                                    form.cleaned_data['created_date'],
                                                                    str(data_dataset['created_date']) +
                                                                    ' 00:00:00+00:00')
                    elif field_to_modify == 'dateModified':
                        variables.sparql_generic_post_object.update_date_leaf(pid, field_to_modify,
                                                                    form.cleaned_data['modified_date'],
                                                                    str(data_dataset['modified_date']) +
                                                                    ' 00:00:00+00:00')
                    elif field_to_modify == 'url-details':
                        variables.sparql_generic_post_object.update_string_leaf(pid, 'url',
                                                                    form.cleaned_data['url_details'],
                                                                    data_dataset['url'])
                    elif field_to_modify == 'url-data-download':
                        variables.sparql_generic_post_object.update_string_leaf(str(pid)+'DD', 'url',
                                                                    form.cleaned_data['url_data'],
                                                                    data_dataset['data_download']['url'])
                    else:
                        variables.sparql_generic_post_object.update_string_leaf(pid, field_to_modify,
                                                                      form.cleaned_data[field_to_modify],
                                                                      data_dataset[field_to_modify])
                    return redirect(dataset_edition, pid=pid)

            context = {
                'form': form,
                'path_name' : ['Données', 'Profil', 'Edition', form.fields[next(iter(form.declared_fields.keys()))].label],
                'path_url' : ['/datasets/', '/datasets/'+pid, '/datasets/edition/'+pid, '/datasets/edition/field/'+field_to_modify+pid],
                'button_value': 'Modifier',
                'url_to_return': '/datasets/edition/field/{}/{}'.format(field_to_modify, pid)
            }
            # return the form to be completed
            return render(request, 'forms/classic_form.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_creator_addition(request, pid):
    '''
    Adds a creator to the given dataset

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page to edit a dataset.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in creators_dataset] or request.user.pid in [maintainers[0] for maintainers in maintainers_dataset]:

            # Check the request method
            if request.method == 'POST':
                creators = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for creator in creators:
                    variables.sparql_post_dataset_object.add_creator_to_dataset(pid, creator.split()[-1])

                return redirect(dataset_edition, pid=pid)

            persons_info = variables.sparql_get_person_object.get_persons()
            persons = []
            for basic_info_person in persons_info:
                if not (basic_info_person[0] in [creator[0] for creator in creators_dataset]):
                    persons.append(
                        '''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Données', 'Profil', 'Edition', 'Ajouter un créateur'],
                'path_url' : ['/datasets/', '/datasets/'+pid, '/datasets/edition/'+pid, '/datasets/edition/field/add-creator/'+pid],
                'title_data_type_added': 'Créateur',
                'data_type_added': 'du créateur',
                'url_to_return': '/datasets/edition/field/add-creator/{}'.format(pid),
                'data': persons
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_creator_deletion(request, pid):
    '''
    Deletes a creator of the given dataset

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a dataset.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in creators_dataset] or request.user.pid in [maintainers[0] for maintainers in maintainers_dataset]:
        
            # Get the value of a variable in the POST request by its id
            creator = request.POST.get('creatorARK', '')
            variables.sparql_post_dataset_object.delete_creator_of_dataset(pid, creator)

            return redirect(dataset_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_maintainer_addition(request, pid):
    '''
    Adds a maintainer to the given dataset

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page to edit a dataset.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in creators_dataset] or request.user.pid in [maintainers[0] for maintainers in maintainers_dataset]:
       
            # Check the request method
            if request.method == 'POST':
                maintainers = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for maintainer in maintainers:
                    variables.sparql_post_dataset_object.add_maintainer_to_dataset(pid, maintainer.split()[-1])

                return redirect(dataset_edition, pid=pid)

            persons_info = variables.sparql_get_person_object.get_persons()
            persons = []
            for basic_info_person in persons_info:
                if not (basic_info_person[0] in [maintainer[0] for maintainer in maintainers_dataset]):
                    persons.append(
                        '''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Données', 'Profil', 'Edition', 'Ajouter un mainteneur'],
                'path_url' : ['/datasets/', '/datasets/'+pid, '/datasets/edition/'+pid, '/datasets/edition/field/add-maintainer/'+pid],
                'title_data_type_added': 'Mainteneur',
                'data_type_added': 'du mainteneur',
                'url_to_return': '/datasets/edition/field/add-maintainer/{}'.format(pid),
                'data': persons
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_maintainer_deletion(request, pid):
    '''
    Deletes a maintainer of the given dataset

    Parameters
    ----------
    request : HttpRequest
        It is the metadata from the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a dataset.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in creators_dataset] or request.user.pid in [maintainers[0] for maintainers in maintainers_dataset]:
       
            # Get the value of a variable in the POST request by its id
            maintainer = request.POST.get('maintainerARK', '')
            variables.sparql_post_dataset_object.delete_maintainer_of_dataset(pid, maintainer)

            return redirect(dataset_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_project_addition(request, pid):
    '''
    Adds a project to the given dataset

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page to edit a dataset.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in creators_dataset] or request.user.pid in [maintainers[0] for maintainers in maintainers_dataset]:
       
            # Check the request method
            if request.method == 'POST':
                projects = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for project in projects:
                    variables.sparql_post_dataset_object.add_project_to_dataset(pid, project.split()[-1])

                return redirect(dataset_edition, pid=pid)

            projects_info = variables.sparql_get_project_object.get_projects()
            projects = []
            # Request all the projects of the dataset
            projects_dataset = variables.sparql_get_dataset_object.get_projects_dataset(pid)
            for basic_info_project in projects_info:
                if not (basic_info_project[0] in [project[0] for project in projects_dataset]):
                    projects.append(
                        '''{}, {}'''.format(basic_info_project[1], basic_info_project[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Données', 'Profil', 'Edition', 'Ajouter un projet'],
                'path_url' : ['/datasets/', '/datasets/'+pid, '/datasets/edition/'+pid, '/datasets/edition/field/add-project/'+pid],
                'title_data_type_added': 'Projet',
                'data_type_added': 'du projet',
                'url_to_return': '/datasets/edition/field/add-project/{}'.format(pid),
                'data': projects
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_project_deletion(request, pid):
    '''
    Deletes a project from the given dataset

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a dataset.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in creators_dataset] or request.user.pid in [maintainers[0] for maintainers in maintainers_dataset]:
       
            project = request.POST.get('projectARK', '')
            variables.sparql_post_dataset_object.delete_project_from_dataset(pid, project)

            return redirect(dataset_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_article_addition(request, pid):
    '''
    Adds an article to the given dataset

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page to edit a dataset.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in creators_dataset] or request.user.pid in [maintainers[0] for maintainers in maintainers_dataset]:
       
            # Check the request method
            if request.method == 'POST':
                articles = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for article in articles:
                    variables.sparql_post_dataset_object.add_article_to_dataset(pid, article.split()[-1])

                return redirect(dataset_edition, pid=pid)

            articles_info = variables.sparql_get_article_object.get_articles()
            articles = []
            # Request all the articles of the dataset
            articles_dataset = variables.sparql_get_dataset_object.get_articles_dataset(pid)
            for basic_info_article in articles_info:
                if not (basic_info_article[0] in [article[0] for article in articles_dataset]):
                    articles.append(
                        '''{}, {}'''.format(basic_info_article[1], basic_info_article[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Données', 'Profil', 'Edition', 'Ajouter un article'],
                'path_url' : ['/datasets/', '/datasets/'+pid, '/datasets/edition/'+pid, '/datasets/edition/field/add-article/'+pid],
                'title_data_type_added': 'Projet',
                'data_type_added': 'du projet',
                'url_to_return': '/datasets/edition/field/add-article/{}'.format(pid),
                'data': articles
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_article_deletion(request, pid):
    '''
    Deletes an article from the given dataset

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a dataset.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in creators_dataset] or request.user.pid in [maintainers[0] for maintainers in maintainers_dataset]:
       
            article = request.POST.get('articleARK', '')
            variables.sparql_post_dataset_object.delete_article_from_dataset(pid, article)

            return redirect(dataset_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_deletion(request, pid):
    '''
    Deletes the given dataset

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the index page.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.is_superuser or request.user.pid in [creators[0] for creators in creators_dataset] or request.user.pid in [maintainers[0] for maintainers in maintainers_dataset]:

            variables.sparql_generic_post_object.delete_subject(pid)
            variables.sparql_generic_post_object.delete_subject(pid+"ARK")
            variables.sparql_generic_post_object.delete_subject(pid+"DD")

            return redirect(views.index)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet dataset"
    }
    return render(request, 'page_info.html', context)
