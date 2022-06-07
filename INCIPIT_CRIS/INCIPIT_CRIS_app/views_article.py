from django.shortcuts import render, redirect
from .forms import *
import re
import string
import json
from . import views
from . import variables
from . import form_selection


def article_results(request,  page=1, filter_category='Articles', filter_letter=''):
    '''
    Search in the triplestore all the articles and format a dictionnary that's used
    in the template to display information.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request
    page : int, optional
        Page to be displayed by the view
    filter_category : str, optional
        Filter to be applied on results to only display articles that belongs to the given category
    filter_letter : str, optional
        Filter to be applied on results to only display articles that begin by the given letter

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display results for articles and a dictionnary with all the data needed to fulfill
        the template.
    '''

    # Defines how many articles will be displayed on the pages
    nb_articles_per_page = 10

    alphabet_list = list(string.ascii_lowercase)
    categories = ['Articles']
    sparql_request = variables.sparql_get_article_object.get_articles()

    if filter_category != '' and filter_category != 'Articles':
        sparql_request = [element for element in sparql_request if filter_category in element]
    if filter_letter != '':
        sparql_request = [element for element in sparql_request if filter_letter == element[1][0].lower()]
    
    last_page = int(len(sparql_request)/nb_articles_per_page)
    if len(sparql_request)%nb_articles_per_page != 0:
        last_page += 1

    context = {
        'path_name' : ['Articles'],
        'path_url' : ['/articles/'],
        'sparql_request': sparql_request[(page-1)*nb_articles_per_page:(page-1)*nb_articles_per_page+nb_articles_per_page],
        'len_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category': filter_category,
        'url':'/articles/',
        'page': page,
        'last_page': last_page,
        'range_pages': range(1, last_page+1),
        'filter_letter': filter_letter,
    }

    return render(request, 'generic/results.html', context)


def article_profile(request, pid):
    '''
    Display a page with all the data of an article that is given by the pid.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the profil of an article and a dictionnary with all the data needed to fulfill
        the template.
    '''

    # Verify in triplestore if the pid correspond to an article
    if variables.sparql_get_article_object.check_article_ark(pid):
        data_article = variables.sparql_get_article_object.get_data_article(pid)
        # Verify if the user as the rights to edit the article
        can_edit = True if request.user.is_authenticated and (request.user.pid in [data_article['authors'][i][1]['pid'] for i in range(len(data_article['authors']))] or request.user.is_superuser) else False

        context = {
            'can_edit': can_edit,
            'data_article': data_article
        }
        return render(request, 'article/article_profile.html', context)

    return render(request, 'page_404.html')


def article_creation(request):
    '''
    Create in the triplestore an article from the data provided from the form requested

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
            form = ArticleCreationForm(request.POST)
            if form.is_valid():
                authors = re.findall('"([^"]*)"', request.POST['authorElementsPost'])
                projects = re.findall('"([^"]*)"', request.POST['projectElementsPost'])
                datasets = re.findall('"([^"]*)"', request.POST['datasetElementsPost'])
                pid = form.cleaned_data['pid']
                if pid == '':
                    try:
                        if request.user.is_superuser:
                            pid = variables.ark.mint(form.cleaned_data['url'], 'Admin',
                                form.cleaned_data['name'], form.cleaned_data['date_published'] if form.cleaned_data['date_published'] != None else '')
                        else:
                            pid = variables.ark.mint(form.cleaned_data['url'], '{} {}'.format(request.user.first_name, request.user.last_name),
                                form.cleaned_data['name'], form.cleaned_data['date_published'] if form.cleaned_data['date_published'] != None else '')
                    except:
                        raise Exception
                variables.sparql_post_article_object.create_article(pid, form.cleaned_data['name'],
                                                          form.cleaned_data['abstract'],
                                                          form.cleaned_data['date_published'], form.cleaned_data['url'])
                for author in authors:
                    variables.sparql_post_article_object.add_author_to_article(pid, author.split()[-1])
                for project in projects:
                    variables.sparql_post_project_object.add_article_to_project(project.split()[-1], pid)
                for dataset in datasets:
                    variables.sparql_post_dataset_object.add_article_to_dataset(dataset.split()[-1], pid)
                if request.POST['institutions'] != '':
                    variables.sparql_post_article_object.add_institution_to_article(pid, request.POST['institutions'])

                return redirect(views.index)
        else:
            form = ArticleCreationForm()
        persons = []
        persons_info = variables.sparql_get_person_object.get_persons()
        for basic_info_person in persons_info:
            persons.append('''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))
        projects_info = variables.sparql_get_project_object.get_projects()
        projects = ['''{}, {}'''.format(project[1], project[0]) for project in projects_info]
        datasets_info = variables.sparql_get_dataset_object.get_datasets()
        datasets = ['''{}, {}'''.format(dataset[1], dataset[0]) for dataset in datasets_info]
        top_lvl_institutions = variables.sparql_get_institution_object.get_top_lvl_institutions()
        top_lvl_institutions_data = []
        for top_lvl_institution in top_lvl_institutions:
            top_lvl_institutions_data.append(variables.sparql_get_institution_object.get_dict_institution(top_lvl_institution[0]))
        context = {
            'form': form,
            'button_value': 'Créer',
            'url_to_return': '/articles/creation/',
            'persons': persons,
            'projects': projects,
            'datasets': datasets,
            'institutions': json.dumps(top_lvl_institutions_data),
        }
        # return the form to be completed
        return render(request, 'forms/article/article_creation.html', context)

    else:
        context = {
            'message': "Connectez-vous pour pourvoir créer des articles"
        }

        return render(request, 'page_info.html', context)


def article_edition(request, pid):
    '''
    Display a page with all the data of the article given by the pid and adds links to modify some parts.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the profil of a article with the fields that can be edited and a dictionnary
        with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the data of the given article
        data_article = variables.sparql_get_article_object.get_data_article(pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in data_article['authors']]:
            context = {
                'data_article': data_article
            }
            return render(request, 'article/article_profile_edition.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_field_edition(request, field_to_modify, pid):
    '''
    Handle the display and the selection of the correct form to modify a given field

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    field_to_modify : str
        Indicates the field that is asked to be modified.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the field of the profil of an article that is going to be modified and a dictionnary
        with all the data needed to fulfill the template.
    '''

    context = {}
    form = forms.Form()
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the data of the given article
        data_article = variables.sparql_get_article_object.get_data_article(pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in data_article['authors']]:

            form = form_selection.form_selection(request, field_to_modify, data_article)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    """try:
                        variables.ark.update(pid, data_article['url'], '{} {}'.format(request.user.first_name, request.user.first_name), data_article['name'], form.cleaned_data['date_published'])
                    except Exception as e:
                        pass # For debugging purposes, for now it does nothing"""

                    if field_to_modify == 'datePublished':
                        date_article = str(data_article['date_published']) + " 00:00:00+00:00" if data_article['date_published'] != 'None' else str(data_article['date_published'])
                        variables.sparql_generic_post_object.update_date_leaf(pid, field_to_modify,
                                                                    form.cleaned_data['date_published'],
                                                                    date_article)
                    else:
                        variables.sparql_generic_post_object.update_string_leaf(pid, field_to_modify,
                                                                      form.cleaned_data[field_to_modify],
                                                                      data_article[field_to_modify])

                    return redirect(article_edition, pid=pid)

            context = {
                'form': form,
                'path_name' : ['Articles', 'Profil', 'Edition', form.fields[next(iter(form.declared_fields.keys()))].label],
                'path_url' : ['/articles/', '/articles/'+pid, '/articles/edition/'+pid, '/articles/edition/field/'+field_to_modify+pid],
                'button_value': 'Modifier',
                'url_to_return': '/articles/edition/field/{}/{}'.format(field_to_modify, pid)
            }
            # return the form to be completed
            return render(request, 'forms/classic_form.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_author_addition(request, pid):
    '''
    Adds an author to the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page to edit an article.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:

            # Check the request method
            if request.method == 'POST':
                authors = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for author in authors:
                    variables.sparql_post_article_object.add_author_to_article(pid, author.split()[-1])

                return redirect(article_edition, pid=pid)

            persons = []
            # Request all the persons in the triplestore
            persons_info = variables.sparql_get_person_object.get_persons()
            for basic_info_person in persons_info:
                if not (basic_info_person[0] in [author[0] for author in authors_article]):
                    persons.append(
                        '''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Articles', 'Profil', 'Edition', 'Ajouter un auteur'],
                'path_url' : ['/articles/', '/articles/'+pid, '/articles/edition/'+pid, '/articles/edition/field/add-author/'+pid],
                'title_data_type_added': 'Auteur',
                'data_type_added': 'du projet',
                'url_to_return': '/articles/edition/field/add-author/{}'.format(pid),
                'data': persons
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_author_deletion(request, pid):
    '''
    Deletes an author of the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of an article.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:
            author = request.POST.get('authorARK', '')
            variables.sparql_post_article_object.delete_author_of_article(pid, author)

            return redirect(article_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_project_addition(request, pid):
    '''
    Adds a project to the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page to edit an article.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles projects to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:

            # Check the request method
            if request.method == 'POST':
                projects = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for project in projects:
                    variables.sparql_post_project_object.add_article_to_project(project.split()[-1], pid)

                return redirect(article_edition, pid=pid)

            projects = []
            # Request all the projects in the triplestore
            projects_info = variables.sparql_get_project_object.get_projects()
            # Request all the projects of the article
            projects_article = variables.sparql_get_article_object.get_projects_article(pid)
            for basic_info_project in projects_info:
                if not (basic_info_project[0] in [project['pid'] for project in projects_article]):
                    projects.append(
                        '''{}, {}'''.format(basic_info_project[1], basic_info_project[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Articles', 'Profil', 'Edition', 'Ajouter un projet'],
                'path_url' : ['/articles/', '/articles/'+pid, '/articles/edition/'+pid, '/articles/edition/field/add-project/'+pid],
                'title_data_type_added': 'Projet',
                'data_type_added': 'du projet',
                'url_to_return': '/articles/edition/field/add-project/{}'.format(pid),
                'data': projects
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_project_deletion(request, pid):
    '''
    Deletes a project of the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of an article.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles projects to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:
            project = request.POST.get('projectARK', '')
            variables.sparql_post_project_object.delete_article_of_project(project, pid)

            return redirect(article_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_dataset_addition(request, pid):
    '''
    Adds a dataset to the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page to edit an article.
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles datasets to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:

            # Check the request method
            if request.method == 'POST':
                datasets = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for dataset in datasets:
                    variables.sparql_post_dataset_object.add_article_to_dataset(dataset.split()[-1], pid)

                return redirect(article_edition, pid=pid)

            datasets = []
            # Request all the datasets in the triplestore
            datasets_info = variables.sparql_get_dataset_object.get_datasets()
            # Request all the datasets of the article
            datasets_article = variables.sparql_get_article_object.get_datasets_article(pid)
            for basic_info_dataset in datasets_info:
                if not (basic_info_dataset[0] in [dataset[0] for dataset in datasets_article]):
                    datasets.append(
                        '''{}, {}'''.format(basic_info_dataset[1], basic_info_dataset[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Articles', 'Profil', 'Edition', 'Ajouter un jeu de données'],
                'path_url' : ['/articles/', '/articles/'+pid, '/articles/edition/'+pid, '/articles/edition/field/add-dataset/'+pid],
                'title_data_type_added': 'Jeu de données',
                'data_type_added': 'du jeu de données',
                'url_to_return': '/articles/edition/field/add-dataset/{}'.format(pid),
                'data': datasets
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_dataset_deletion(request, pid):
    '''
    Deletes a dataset of the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of an article.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles datasets to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:
            dataset = request.POST.get('datasetARK', '')
            variables.sparql_post_dataset_object.delete_article_from_dataset(dataset, pid)

            return redirect(article_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_institution_addition(request, pid):
    '''
    Adds an institution to the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of an article.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles datasets to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:

            # Check the request method
            if request.method == 'POST':
                variables.sparql_post_article_object.add_institution_to_article(pid, request.POST['institutions'])

                return redirect(article_edition, pid=pid)

            top_lvl_institutions = variables.sparql_get_institution_object.get_top_lvl_institutions()
            top_lvl_institutions_data = []
            for top_lvl_institution in top_lvl_institutions:
                top_lvl_institutions_data.append(variables.sparql_get_institution_object.get_dict_institution(top_lvl_institution[0]))

            context = {
                'button_value': 'Ajouter',
                'path_name' : ['Articles', 'Profil', 'Edition', 'Ajouter un jeu de données'],
                'path_url' : ['/articles/', '/articles/'+pid, '/articles/edition/'+pid, '/articles/edition/field/add-institution/'+pid],
                'title_data_type_added': 'Institution',
                'data_type_added': 'de l\'institution',
                'url_to_return': '/articles/edition/field/add-institution/{}'.format(pid),
                'institutions': json.dumps(top_lvl_institutions_data),
            }
            # return the form to be completed
            return render(request, 'forms/select_institution_form.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_institution_deletion(request, pid):
    '''
    Deletes a institution of the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of an article.
        HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles institutions to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:
            institution = request.POST.get('institutionARK', '')
            variables.sparql_post_article_object.delete_institution_from_article(pid, institution)

            return redirect(article_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_doi_addition(request, pid):
    '''
    Adds a doi to the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a article.
    '''
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles institutions to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:
            doi = variables.sparql_get_article_object.get_DOI_article(pid)
            # Check the request method
            if request.method == 'POST':
                form = URLForm(request.POST)
                if form.is_valid():
                    doi_data = form.cleaned_data['url']
                    if doi_data != '':
                        variables.sparql_post_article_object.add_DOI_article(pid, doi_data)

                    return redirect(article_edition, pid=pid)
            
            form = URLForm(old_url=doi)

            context = {
                'form': form,
                'path_name' : ['Articles', 'Profil', 'Edition', 'Ajouter un identifiant DOI'],
                'path_url' : ['/articles/', '/articles/'+pid, '/articles/edition/'+pid, '/articles/edition/profil/add-doi/'+pid],
                'title_data_type_added': 'Ajouter un identifiant DOI',
                'data_type_added': 'Identifiant DOI',
                'url_to_return': '/articles/edition/field/add-doi/{}'.format(pid),
                'button_value': 'Ajouter',
            }

            form.fields['url'].widget.attrs.update({'placeholder':context['data_type_added']})

            return render(request, 'forms/edited_form.html', context)
    
        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def article_doi_deletion(request, pid):
    '''
    Delete the doi url of the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a article.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles institutions to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:

            # Get the value of a variable in the POST request by its id
            doi = request.POST.get('doi', '')
            variables.sparql_post_article_object.delete_DOI_article(pid, doi)

            return redirect(article_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def article_deletion(request, pid):
    '''
    Deletes the given article

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: str
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
        # Request all the authors of the article
        authors_article = variables.sparql_get_article_object.get_authors_article(pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.is_superuser or request.user.pid in [authors[0] for authors in authors_article]:
            variables.sparql_generic_post_object.delete_subject(pid)
            variables.sparql_generic_post_object.delete_object(pid)
            variables.sparql_generic_post_object.delete_subject(pid+"ARK")
            variables.sparql_generic_post_object.delete_object(pid+"ARK")

            return redirect(views.index)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)
