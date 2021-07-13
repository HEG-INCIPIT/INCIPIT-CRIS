from django.shortcuts import render, redirect
from .forms import *
import string
import re
from . import variables


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
    categories = ['Personnes', 'Professeurs ordinaire', 'Assistants HES']
    category = categories[0]
    sparql_request = variables.sparql_get_person_object.get_persons()
    context = {
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
    }

    return render(request, 'person/person_results.html', context)


def person_profile(request, ark_pid):
    '''
    Display a page with all the data of a person that is given by the ark_pid.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the profil of a person and a dictionnary with all the data needed to fulfill
        the template.
    '''

    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = variables.sparql_get_person_object.check_person_ark(ark_pid)
    can_edit = True if request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser) else False
    if sparql_request_check_person_ark:
        data_person = variables.sparql_get_person_object.get_data_person(ark_pid)

        # Some elements contained in the dictionnary data_person :
        #
        #data_person['articles'] : all data of articles for whom the person is author
        #data_person['projects'] : all data of projects for whom the person is member

        context = {
            'data_person': data_person,
            'can_edit': can_edit,
            'ark_pid': ark_pid,
        }
        return render(request, 'person/person_profile.html', context)

    return render(request, 'page_404.html')


def person_edition(request, ark_pid):
    '''
    Display a page with all the data of the person given by the ark_pid and adds links to modify some parts.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the profil of a person with the fields that can be edited and a dictionnary
        with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = variables.sparql_get_person_object.check_person_ark(ark_pid)
    if sparql_request_check_person_ark:
        if request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser):
            data_person = variables.sparql_get_person_object.get_data_person(ark_pid)
            context = {
                'data_person': data_person,
                'ark_pid': ark_pid
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


def person_form_selection(request, part_of_person_to_modify, data_person):
    '''
    Select and return the correct form to be used in order to modify a field.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    part_of_person_to_modify : String
        Indicates the field that is asked to be modified.
    data_person : Dictionary
        Contain the data of the different fields of a person.

    Returns
    -------
    Form
        A form with the fields desired
    '''
    # Check the request method
    if request.method == 'POST':
        if part_of_person_to_modify == 'description':
            return DescriptionForm(request.POST)
        if part_of_person_to_modify == 'telephone':
            return TelephoneForm(request.POST)

    # if not a POST it'll create a blank form
    else:
        if part_of_person_to_modify == 'description':
            return DescriptionForm(old_description=data_person[part_of_person_to_modify])
        if part_of_person_to_modify == 'telephone':
            return TelephoneForm(old_telephone=data_person[part_of_person_to_modify])


def person_field_edition(request, part_of_person_to_modify, ark_pid):
    '''
    Handle the display and the selection of the correct form to modify a given field

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    part_of_person_to_modify : String
        Indicates the field that is asked to be modified.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the field of the profil of a person that is going to be modified and a dictionnary
        with all the data needed to fulfill the template.
    '''
    
    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = variables.sparql_get_person_object.check_person_ark(ark_pid)

    if sparql_request_check_person_ark:
        # Verify that the user is authenticated and has the right to modify the profile
        if request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser):

            data_person = variables.sparql_get_person_object.get_data_person(ark_pid)

            form = person_form_selection(request, part_of_person_to_modify, data_person)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    variables.sparql_generic_post_object.update_string_leaf(ark_pid, part_of_person_to_modify,
                                                                  form.cleaned_data[part_of_person_to_modify],
                                                                  data_person[part_of_person_to_modify])
                    return redirect(person_edition, ark_pid=ark_pid)

            context = {
                'form': form,
                'button_value': 'Modifier',
                'url_to_return': '/personnes/edition/profil/{}/{}'.format(part_of_person_to_modify, ark_pid)
            }
            # return the form to be completed
            return render(request, 'forms/classic_form.html', context)

        else:
            # Check why the person cannot modify the profile and display the error
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


def person_article_deletion(request, ark_pid):
    '''
    Deletes an article of the given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.ark_pid == ark_pid or request.user.is_superuser:
            article = request.POST.get('articleARK', '')
            variables.sparql_post_article_object.delete_author_of_article(article, ark_pid)

            return redirect(person_edition, ark_pid=ark_pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def person_article_addition(request, ark_pid):
    context = {}
    
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify if the user as the right to modify the profile
        if request.user.ark_pid == ark_pid or request.user.is_superuser:
            
            # Check the request method
            if request.method == 'POST':
                articles = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for article in articles:
                    variables.sparql_post_article_object.add_author_to_article(article.split()[-1], ark_pid)

                return redirect(person_edition, ark_pid=ark_pid)

            articles_info = variables.sparql_get_article_object.get_articles()
            articles = []
            # Request all the articles of the person
            articles_person = variables.sparql_get_person_object.get_articles_person(ark_pid)
            for basic_info_article in articles_info:
                if not (basic_info_article[0] in [article[0] for article in articles_person]):
                    articles.append(
                        '''{}, {}'''.format(basic_info_article[1], basic_info_article[0]))

            context = {
                'button_value': 'Ajouter',
                'title_data_type_added': 'Article',
                'data_type_added': 'de l\'article',
                'url_to_return': '/personnes/edition/profil/add-article/{}'.format(ark_pid),
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


def person_project_addition(request, ark_pid):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify if the user as the right to modify the profile
        if request.user.ark_pid == ark_pid or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                projects = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for project in projects:
                    variables.sparql_post_project_object.add_member_to_project(project.split()[-1], ark_pid)

                return redirect(person_edition, ark_pid=ark_pid)

            projects_info = variables.sparql_get_project_object.get_projects()
            projects = []
            # Request all the projects of the person
            projects_person = variables.sparql_get_person_object.get_projects_person(ark_pid)
            for basic_info_project in projects_info:
                if not (basic_info_project[0] in [project[0] for project in projects_person]):
                    projects.append(
                        '''{}, {}'''.format(basic_info_project[1], basic_info_project[0]))

            context = {
                'button_value': 'Ajouter',
                'title_data_type_added': 'Projet',
                'data_type_added': 'du projet',
                'url_to_return': '/personnes/edition/profil/add-project/{}'.format(ark_pid),
                'data': projects
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet person",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet person"
    }
    return render(request, 'page_info.html', context)


def person_project_deletion(request, ark_pid):
    '''
    Deletes a project of the given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.ark_pid == ark_pid or request.user.is_superuser:
            project = request.POST.get('projectARK', '')
            variables.sparql_post_project_object.delete_member_of_project(project, ark_pid)

            return redirect(person_edition, ark_pid=ark_pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def person_datasets_creator_addition(request, ark_pid):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify if the user as the right to modify the profile
        if request.user.ark_pid == ark_pid or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                datasets = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for dataset in datasets:
                    variables.sparql_post_dataset_object.add_creator_to_dataset(dataset.split()[-1], ark_pid)

                return redirect(person_edition, ark_pid=ark_pid)

            datasets_info = variables.sparql_get_dataset_object.get_datasets()
            datasets = []
            # Request all the datasets of the person
            datasets_person = variables.sparql_get_person_object.get_datasets_creator_person(ark_pid)
            for basic_info_dataset in datasets_info:
                if not (basic_info_dataset[0] in [dataset[0] for dataset in datasets_person]):
                    datasets.append(
                        '''{}, {}'''.format(basic_info_dataset[1], basic_info_dataset[0]))

            context = {
                'button_value': 'Ajouter',
                'title_data_type_added': 'Jeu de données',
                'data_type_added': 'du jeu de données',
                'url_to_return': '/personnes/edition/profil/add-dataset-creator/{}'.format(ark_pid),
                'data': datasets
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet person",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet person"
    }
    return render(request, 'page_info.html', context)


def person_datasets_creator_deletion(request, ark_pid):
    '''
    Deletes a dataset of the given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.ark_pid == ark_pid or request.user.is_superuser:

            dataset = request.POST.get('dataset_creatorARK', '')
            print("LAAAAAAAAAAAAAAAAAAAAAA")
            variables.sparql_post_dataset_object.delete_creator_of_dataset(dataset, ark_pid)

            return redirect(person_edition, ark_pid=ark_pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce dataset"
    }
    return render(request, 'page_info.html', context)


def person_datasets_maintainer_addition(request, ark_pid):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify if the user as the right to modify the profile
        if request.user.ark_pid == ark_pid or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                datasets = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for dataset in datasets:
                    variables.sparql_post_dataset_object.add_maintainer_to_dataset(dataset.split()[-1], ark_pid)

                return redirect(person_edition, ark_pid=ark_pid)

            datasets_info = variables.sparql_get_dataset_object.get_datasets()
            datasets = []
            # Request all the datasets of the person
            datasets_person = variables.sparql_get_person_object.get_datasets_maintainer_person(ark_pid)
            for basic_info_dataset in datasets_info:
                if not (basic_info_dataset[0] in [dataset[0] for dataset in datasets_person]):
                    datasets.append(
                        '''{}, {}'''.format(basic_info_dataset[1], basic_info_dataset[0]))

            context = {
                'button_value': 'Ajouter',
                'title_data_type_added': 'Jeu de données',
                'data_type_added': 'du jeu de données',
                'url_to_return': '/personnes/edition/profil/add-dataset-maintainer/{}'.format(ark_pid),
                'data': datasets
            }
            # return the form to be completed
            return render(request, 'forms/autocompletion_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet person",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet person"
    }
    return render(request, 'page_info.html', context)


def person_datasets_maintainer_deletion(request, ark_pid):
    '''
    Deletes a dataset of the given person

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a person.
    '''
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.ark_pid == ark_pid or request.user.is_superuser:

            dataset = request.POST.get('dataset_maintainerARK', '')
            print("ICIIIIIIIIIIIIIIII")
            variables.sparql_post_dataset_object.delete_maintainer_of_dataset(dataset, ark_pid)

            return redirect(person_edition, ark_pid=ark_pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce dataset"
    }
    return render(request, 'page_info.html', context)
