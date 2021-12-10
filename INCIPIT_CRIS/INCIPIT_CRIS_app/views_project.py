from django.shortcuts import render, redirect
from .forms import *
import re
import string
import json
from django.conf import settings
from . import views
from . import variables
from . import form_selection


def project_results(request, page=1, filter_category='Projets', filter_letter=''):
    '''
    Search in the triplestore all the projects and format a dictionnary that's used
    in the template to display information.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display results for projects and a dictionnary with all the data needed to fulfill
        the template.
    '''

    # Defines how many projects will be displayed on the pages
    nb_projects_per_page = 10

    alphabet_list = list(string.ascii_lowercase)
    categories = ['Projets']
    sparql_request = variables.sparql_get_project_object.get_projects()

    if filter_category != '' and filter_category != 'Projets':
        sparql_request = [element for element in sparql_request if filter_category in element]
    if filter_letter != '':
        sparql_request = [element for element in sparql_request if filter_letter == element[1][0].lower()]
    
    last_page = int(len(sparql_request)/nb_projects_per_page)
    if len(sparql_request)%nb_projects_per_page != 0:
        last_page += 1

    context = {
        'path_name' : ['Projets'],
        'path_url' : ['/projects/'],
        'sparql_request': sparql_request[(page-1)*nb_projects_per_page:(page-1)*nb_projects_per_page+nb_projects_per_page],
        'len_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category': filter_category,
        'url':'/projects/',
        'page': page,
        'last_page': last_page,
        'range_pages': range(1, last_page+1),
        'filter_letter': filter_letter,
    }

    return render(request, 'generic/results.html', context)


def project_creation(request):
    '''
    Create a project in the triplestore and mint an ARK if it's not given

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    form = forms.Form()
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Check the request method
        if request.method == 'POST':
            form = ProjectCreationForm(request.POST)
            if form.is_valid():
                members = re.findall('"([^"]*)"', request.POST['memberElementsPost'])
                articles = re.findall('"([^"]*)"', request.POST['articleElementsPost'])
                datasets = re.findall('"([^"]*)"', request.POST['datasetElementsPost'])
                pid = form.cleaned_data['pid']
                if pid == '':
                    # Try to mint an ARK with the functions of the app arketype_API
                    try:
                        if request.user.is_superuser:
                            pid = variables.ark.mint(form.cleaned_data['url'], 'Admin',
                                form.cleaned_data['name'], form.cleaned_data['founding_date'] if form.cleaned_data['founding_date'] != None else '')
                        else:
                            pid = variables.ark.mint(form.cleaned_data['url'], '{} {}'.format(request.user.first_name, request.user.last_name),
                                form.cleaned_data['name'], form.cleaned_data['founding_date'] if form.cleaned_data['founding_date'] != None else '')
                    except:
                        raise Exception
                variables.sparql_post_project_object.create_project(pid, form.cleaned_data['name'],
                                                        form.cleaned_data['description'],
                                                        form.cleaned_data['founding_date'], form.cleaned_data['dissolution_date'], form.cleaned_data['url'], form.cleaned_data['url_logo'])
                for member in members:
                    variables.sparql_post_project_object.add_member_to_project(pid, member.split()[-1])
                for article in articles:
                    variables.sparql_post_project_object.add_article_to_project(pid, article.split()[-1])
                for dataset in datasets:
                    variables.sparql_post_dataset_object.add_project_to_dataset(dataset.split()[-1], pid)

                if request.POST['institutions'] != '':
                    variables.sparql_post_project_object.add_institution_to_project(pid, request.POST['institutions'])

                if request.POST['funders'] != '':
                    variables.sparql_post_funder_object.add_project_to_funder(request.POST['funders'], pid)

                return redirect(views.index)
        else:
            form = ProjectCreationForm()
        persons_info = variables.sparql_get_person_object.get_persons()
        persons = []
        for basic_info_person in persons_info:
            persons.append('''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))
        articles_info = variables.sparql_get_article_object.get_articles()
        articles = ['''{}, {}'''.format(article[1], article[0]) for article in articles_info]
        datasets_info = variables.sparql_get_dataset_object.get_datasets()
        datasets = ['''{}, {}'''.format(dataset[1], dataset[0]) for dataset in datasets_info]
        top_lvl_institutions = variables.sparql_get_institution_object.get_top_lvl_institutions()
        top_lvl_institutions_data = []
        for top_lvl_institution in top_lvl_institutions:
            top_lvl_institutions_data.append(variables.sparql_get_institution_object.get_dict_institution(top_lvl_institution[0]))
        funders = variables.sparql_get_funder_object.get_funders()
        context = {
            'form': form,
            'button_value': 'Créer',
            'url_to_return': '/projects/creation/',
            'persons': persons,
            'articles': articles,
            'datasets': datasets,
            'institutions': json.dumps(top_lvl_institutions_data),
            'funders': funders,
        }
        # return the form to be completed
        return render(request, 'forms/project/project_creation.html', context)

    else:
        context = {
            'message': "Connectez-vous pour pourvoir créer des projets"
        }

        return render(request, 'page_info.html', context)


def project_profile(request, pid):
    '''
    Display a page with all the data of a project that is given by the pid.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify in triplestore if the pid correspond to a project
    sparql_request_check_project_ark = variables.sparql_get_project_object.check_project_ark(pid)
    if sparql_request_check_project_ark:
        data_project = variables.sparql_get_project_object.get_data_project(pid)
        can_edit = True if request.user.is_authenticated and (request.user.pid in [data_project['members'][i][1]['pid'] for i in range(len(data_project['members']))] or request.user.is_superuser) else False
        context = {
            'data_project': data_project,
            'can_edit': can_edit,
        }
        return render(request, 'project/project_profile.html', context)

    return render(request, 'page_404.html')

def project_edition(request, pid):
    '''
    Display a page with all the data of the project given by the pid and adds links to modify some parts.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the data of the given project
        data_project = variables.sparql_get_project_object.get_data_project(pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.is_superuser or request.user.pid in [members[0] for members in data_project['members']]:
            context = {
                'data_project': data_project
            }
            return render(request, 'project/project_profile_edition.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def project_field_edition(request, field_to_modify, pid):
    '''
    Handle the display and the selection of the correct form to modify a given field

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    part_of_project_to_modify : String
        Indicates the field that is asked to be modified.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the field of the profil of a project that is going to be modified and a dictionnary
        with all the data needed to fulfill the template.
    '''

    context = {}
    form = forms.Form()
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:

            data_project = variables.sparql_get_project_object.get_data_project(pid)

            form = form_selection.form_selection(request, field_to_modify, data_project)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    if field_to_modify == 'foundingDate':
                        date_project = str(data_project['founding_date']) + " 00:00:00+00:00" if data_project['founding_date'] != 'None' else str(data_project['founding_date'])
                        variables.sparql_generic_post_object.update_date_leaf(pid, field_to_modify,
                                                                    form.cleaned_data['founding_date'],
                                                                    date_project)
                    elif field_to_modify == 'dissolutionDate':
                        date_project = str(data_project['dissolution_date']) + " 00:00:00+00:00" if data_project['dissolution_date'] != 'None' else str(data_project['dissolution_date'])
                        variables.sparql_generic_post_object.update_date_leaf(pid, field_to_modify,
                                                                    form.cleaned_data['dissolution_date'],
                                                                    date_project)
                    elif field_to_modify == 'logo':
                        variables.sparql_generic_post_object.update_string_leaf(pid, field_to_modify,
                                                                      form.cleaned_data['url'],
                                                                      data_project[field_to_modify])
                    else:
                        variables.sparql_generic_post_object.update_string_leaf(pid, field_to_modify,
                                                                      form.cleaned_data[field_to_modify],
                                                                      data_project[field_to_modify])
                    return redirect(project_edition, pid=pid)

            context = {
                'form': form,
                'path_name' : ['Projets', 'Profil', 'Edition', form.fields[next(iter(form.declared_fields.keys()))].label],
                'path_url' : ['/projects/', '/projects/'+pid, '/projects/edition/'+pid, '/projects/edition/field/'+field_to_modify+pid],
                'button_value': 'Modifier',
                'url_to_return': '/projects/edition/field/{}/{}'.format(field_to_modify, pid)
            }
            # return the form to be completed
            return render(request, 'forms/classic_form.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def project_member_addition(request, pid):
    '''
    Adds a member to the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page to edit a project.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:

            data_project = variables.sparql_get_project_object.get_data_project(pid)
            # Check the request method
            if request.method == 'POST':
                members = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for member in members:
                    variables.sparql_post_project_object.add_member_to_project(pid, member.split()[-1])

                return redirect(project_edition, pid=pid)

            persons_info = variables.sparql_get_person_object.get_persons()
            persons = []
            for basic_info_person in persons_info:
                if not (basic_info_person[0] in [member[0] for member in members_project]):
                    persons.append(
                        '''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Projets', 'Profil', 'Edition', 'Ajouter un membre'],
                'path_url' : ['/projects/', '/projects/'+pid, '/projects/edition/'+pid, '/projects/edition/field/add-member/'+pid],
                'title_data_type_added': 'Membre',
                'data_type_added': 'du membre',
                'url_to_return': '/projects/edition/field/add-member/{}'.format(pid),
                'data': persons
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def project_member_deletion(request, pid):
    '''
    Deletes a member of the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:
            member = request.POST.get('memberARK', '')
            variables.sparql_post_project_object.delete_member_of_project(pid, member)

            return redirect(project_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def project_article_addition(request, pid):
    '''
    Adds an article to the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects articles to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                articles = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for article in articles:
                    variables.sparql_post_project_object.add_article_to_project(pid, article.split()[-1])

                return redirect(project_edition, pid=pid)

            articles_info = variables.sparql_get_article_object.get_articles()
            articles = []
            # Request all the articles of the project
            articles_project = variables.sparql_get_project_object.get_articles_project(pid)
            for basic_info_article in articles_info:
                if not (basic_info_article[0] in [article[0] for article in articles_project]):
                    articles.append(
                        '''{}, {}'''.format(basic_info_article[1], basic_info_article[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Projets', 'Profil', 'Edition', 'Ajouter un article'],
                'path_url' : ['/projects/', '/projects/'+pid, '/projects/edition/'+pid, '/projects/edition/field/add-article/'+pid],
                'title_data_type_added': 'Article',
                'data_type_added': 'de l\'article',
                'url_to_return': '/projects/edition/field/add-article/{}'.format(pid),
                'data': articles
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def project_article_deletion(request, pid):
    '''
    Deletes an article of the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:
            article = request.POST.get('articleARK', '')
            variables.sparql_post_project_object.delete_article_of_project(pid, article)

            return redirect(project_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def project_dataset_addition(request, pid):
    '''
    Adds a dataset to the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects datasets to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                datasets = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for dataset in datasets:
                    variables.sparql_post_dataset_object.add_project_to_dataset(dataset.split()[-1], pid)

                return redirect(project_edition, pid=pid)

            datasets_info = variables.sparql_get_dataset_object.get_datasets()
            datasets = []
            # Request all the datasets of the project
            datasets_project = variables.sparql_get_project_object.get_datasets_project(pid)
            for basic_info_dataset in datasets_info:
                if not (basic_info_dataset[0] in [dataset[0] for dataset in datasets_project]):
                    datasets.append(
                        '''{}, {}'''.format(basic_info_dataset[1], basic_info_dataset[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Projets', 'Profil', 'Edition', 'Ajouter un jeu de données'],
                'path_url' : ['/projects/', '/projects/'+pid, '/projects/edition/'+pid, '/projects/edition/field/add-dataset/'+pid],
                'title_data_type_added': 'Jeu de données',
                'data_type_added': 'du jeu de données',
                'url_to_return': '/projects/edition/field/add-dataset/{}'.format(pid),
                'data': datasets
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce project"
    }
    return render(request, 'page_info.html', context)


def project_dataset_deletion(request, pid):
    '''
    Deletes an dataset of the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:
            dataset = request.POST.get('datasetARK', '')
            variables.sparql_post_dataset_object.delete_project_from_dataset(dataset, pid)

            return redirect(project_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce project"
    }
    return render(request, 'page_info.html', context)


def project_institution_addition(request, pid):
    '''
    Adds a institution to the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects institutions to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                variables.sparql_post_project_object.add_institution_to_project(pid, request.POST['institutions'])

                return redirect(project_edition, pid=pid)

            top_lvl_institutions = variables.sparql_get_institution_object.get_top_lvl_institutions()
            top_lvl_institutions_data = []
            for top_lvl_institution in top_lvl_institutions:
                top_lvl_institutions_data.append(variables.sparql_get_institution_object.get_dict_institution(top_lvl_institution[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Projets', 'Profil', 'Edition', 'Ajouter une institution'],
                'path_url' : ['/projects/', '/projects/'+pid, '/projects/edition/'+pid, '/projects/edition/field/add-institution/'+pid],
                'title_data_type_added': 'Institutions',
                'data_type_added': 'de l\'institution',
                'url_to_return': '/projects/edition/field/add-institution/{}'.format(pid),
                'institutions': json.dumps(top_lvl_institutions_data),
            }
            # return the form to be completed
            return render(request, 'forms/select_institution_form.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce project"
    }
    return render(request, 'page_info.html', context)


def project_institution_deletion(request, pid):
    '''
    Deletes an institution of the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:
            institution = request.POST.get('institutionARK', '')
            variables.sparql_post_project_object.delete_institution_from_project(pid, institution)

            return redirect(project_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce project"
    }
    return render(request, 'page_info.html', context)


def project_funder_addition(request, pid):
    '''
    Adds a funder to the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects funders to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                variables.sparql_post_project_object.add_funder_to_project(pid, request.POST['funders'])

                return redirect(project_edition, pid=pid)

            funders = variables.sparql_get_funder_object.get_funders()

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Projets', 'Profil', 'Edition', 'Ajouter une funder'],
                'path_url' : ['/projects/', '/projects/'+pid, '/projects/edition/'+pid, '/projects/edition/field/add-funder/'+pid],
                'title_data_type_added': 'Bailleur de fonds',
                'data_type_added': 'du bailleur de fonds',
                'url_to_return': '/projects/edition/field/add-funder/{}'.format(pid),
                'funders': funders,
            }
            # return the form to be completed
            return render(request, 'forms/select_funder_form.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce project"
    }
    return render(request, 'page_info.html', context)


def project_funder_deletion(request, pid):
    '''
    Deletes an funder of the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:
            funder = request.POST.get('funderARK', '')
            variables.sparql_post_project_object.delete_funder_from_project(pid, funder)

            return redirect(project_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce project"
    }
    return render(request, 'page_info.html', context)


def project_deletion(request, pid):
    '''
    Deletes completely an project and all his leafs

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirects to the index page or renders a page with
        information on why the it's not possible to delete the project.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.pid in [members[0] for members in members_project] or request.user.is_superuser:
            variables.sparql_generic_post_object.delete_subject(pid)
            variables.sparql_generic_post_object.delete_object(pid)
            variables.sparql_generic_post_object.delete_subject(pid+"ARK")
            variables.sparql_generic_post_object.delete_object(pid+"ARK")

            return redirect(views.index)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet projet",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet projet"
    }
    return render(request, 'page_info.html', context)
