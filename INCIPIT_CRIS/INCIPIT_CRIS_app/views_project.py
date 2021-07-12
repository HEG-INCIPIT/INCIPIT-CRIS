from django.shortcuts import render, redirect
from .forms import *
import re
import string
import datetime
from django.conf import settings
from . import views
from . import variables


def project_results(request):
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

    alphabet_list = list(string.ascii_lowercase)
    categories = ['Projets de recherche']
    category = categories[0]
    sparql_request = variables.sparql_get_project_object.get_projects()
    context = {
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
        'url':'/projects/',
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
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Check the request method
        if request.method == 'POST':
            form = ProjectCreationForm(request.POST)
            if form.is_valid():
                members = re.findall('"([^"]*)"', request.POST['memberElementsPost'])
                ark_pid = form.cleaned_data['ark_pid']
                if ark_pid == '':
                    # Try to mint an ARK with the functions of the app arketype_API
                    try:
                        ark_pid = variables.ark.mint('', '{}'.format(form.cleaned_data['name']), 
                            'Creating an ARK in INCIPIT-CRIS for a project named {}'.format(form.cleaned_data['name']), '{}'.format(datetime.datetime.now()))
                        variables.ark.update('{}'.format(ark_pid), '{}{}'.format(settings.URL, ark_pid), '{} {}'.format(form.cleaned_data['name']), 
                            'Creating an ARK in INCIPIT-CRIS for an project named {}'.format(form.cleaned_data['name']), '{}'.format(datetime.datetime.now()))
                    except:
                        print("ERROR")
                        raise Exception
                variables.sparql_post_project_object.create_project(ark_pid, form.cleaned_data['name'],
                                                        form.cleaned_data['description'],
                                                        form.cleaned_data['founding_date'], form.cleaned_data['dissolution_date'], form.cleaned_data['url'])
                for member in members:
                    variables.sparql_post_project_object.add_member_to_project(ark_pid, member.split()[-1])
                return redirect(views.index)
        else:
            form = ProjectCreationForm()
        persons_info = variables.sparql_get_person_object.get_persons()
        persons = []
        for basic_info_person in persons_info:
            persons.append('''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))
        context = {
            'form': form,
            'button_value': 'Créer',
            'url_to_return': '/projects/creation/',
            'persons': persons
        }
        # return the form to be completed
        return render(request, 'forms/project/project_creation.html', context)

    else:
        context = {
            'message': "Connectez-vous pour pourvoir créer des projets"
        }

        return render(request, 'page_info.html', context)


def project_profile(request, ark_pid):
    '''
    Display a page with all the data of a project that is given by the ark_pid.

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
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify in triplestore if the ark_pid correspond to a project
    sparql_request_check_project_ark = variables.sparql_get_project_object.check_project_ark(ark_pid)
    if sparql_request_check_project_ark:
        data_project = variables.sparql_get_project_object.get_data_project(ark_pid)
        edition_granted = False
        if request.user.is_authenticated and request.user.ark_pid in [members[0] for members in data_project['members']]:
            edition_granted = True
        context = {
            'edition_granted': edition_granted,
            'data_project': data_project
        }
        return render(request, 'project/project_profile.html', context)

    return render(request, 'page_404.html')

def project_edition(request, ark_pid):
    '''
    Display a page with all the data of the project given by the ark_pid and adds links to modify some parts.

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
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:
            edition_granted = True
            data_project = variables.sparql_get_project_object.get_data_project(ark_pid)
            context = {
                'edition_granted': edition_granted,
                'data_project': data_project
            }
            return render(request, 'project/project_profile_edition.html', context)

        edition_granted = False
        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
            'edition_granted': edition_granted
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def project_form_selection(request, part_of_project_to_edit, data_project):
    '''
    Select and return the correct form to be used in order to modify a field.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    part_of_project_to_modify : String
        Indicates the field that is asked to be modified.
    data_project : Dictionary
        Contain the data of the different fields of a project.

    Returns
    -------
    Form
        A form with the fields desired
    '''

    # Check the request method
    if request.method == 'POST':
        if part_of_project_to_edit == 'name':
            return ProjectNameForm(request.POST)
        if part_of_project_to_edit == 'description':
            return ProjectDescriptionForm(request.POST)
        if part_of_project_to_edit == 'foundingDate':
            return ProjectFoundingDateForm(request.POST)
        if part_of_project_to_edit == 'dissolutionDate':
            return ProjectDissolutionDateForm(request.POST)
        if part_of_project_to_edit == 'url':
            return URLForm(request.POST)

    # if not a POST it'll create a blank form
    else:
        if part_of_project_to_edit == 'name':
            return ProjectNameForm(old_name=data_project[part_of_project_to_edit])
        if part_of_project_to_edit == 'description':
            return ProjectDescriptionForm(old_description=data_project[part_of_project_to_edit])
        if part_of_project_to_edit == 'foundingDate':
            return ProjectFoundingDateForm(old_founding_date=data_project['founding_date'])
        if part_of_project_to_edit == 'dissolutionDate':
            return ProjectDissolutionDateForm(old_dissolution_date=data_project['dissolution_date'])
        if part_of_project_to_edit == 'url':
            return URLForm(old_url=data_project['url'])


def project_field_edition(request, part_of_project_to_edit, ark_pid):
    '''
    Handle the display and the selection of the correct form to modify a given field

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    part_of_project_to_modify : String
        Indicates the field that is asked to be modified.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the field of the profil of a project that is going to be modified and a dictionnary
        with all the data needed to fulfill the template.
    '''
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:

            data_project = variables.sparql_get_project_object.get_data_project(ark_pid)

            form = project_form_selection(request, part_of_project_to_edit, data_project)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    if part_of_project_to_edit == 'foundingDate':
                        variables.sparql_generic_post_object.update_date_leaf(ark_pid, part_of_project_to_edit,
                                                                    form.cleaned_data['founding_date'],
                                                                    str(data_project['founding_date']) +
                                                                    " 00:00:00+00:00")
                    elif part_of_project_to_edit == 'dissolutionDate':
                        variables.sparql_generic_post_object.update_date_leaf(ark_pid, part_of_project_to_edit,
                                                                    form.cleaned_data['dissolution_date'],
                                                                    str(data_project['dissolution_date']) +
                                                                    " 00:00:00+00:00")
                    else:
                        variables.sparql_generic_post_object.update_string_leaf(ark_pid, part_of_project_to_edit,
                                                                      form.cleaned_data[part_of_project_to_edit],
                                                                      data_project[part_of_project_to_edit])
                    return redirect(project_edition, ark_pid=ark_pid)

            context = {
                'form': form,
                'button_value': 'Modifier',
                'url_to_return': '/projects/edition/field/{}/{}'.format(part_of_project_to_edit, ark_pid)
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


def project_member_addition(request, ark_pid):
    '''
    Adds a member to the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
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
        members_project = variables.sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:

            data_project = variables.sparql_get_project_object.get_data_project(ark_pid)
            # Check the request method
            if request.method == 'POST':
                members = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for member in members:
                    variables.sparql_post_project_object.add_member_to_project(ark_pid, member.split()[-1])

                return redirect(project_edition, ark_pid=ark_pid)

            persons_info = variables.sparql_get_person_object.get_persons()
            persons = []
            for basic_info_person in persons_info:
                if not (basic_info_person[0] in [member[0] for member in members_project]):
                    persons.append(
                        '''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))

            context = {
                'button_value': 'Ajouter',
                'title_data_type_added': 'Membre',
                'data_type_added': 'du membre',
                'url_to_return': '/projects/edition/field/add-member/{}'.format(ark_pid),
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


def project_member_deletion(request, ark_pid):
    '''
    Deletes a member of the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
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
        members_project = variables.sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:
            member = request.POST.get('memberARK', '')
            variables.sparql_post_project_object.delete_member_of_project(ark_pid, member)

            return redirect(project_edition, ark_pid=ark_pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def project_article_addition(request, ark_pid):
    '''
    Adds an article to the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
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
        members_project = variables.sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects articles to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                articles = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for article in articles:
                    variables.sparql_post_project_object.add_article_to_project(ark_pid, article.split()[-1])

                return redirect(project_edition, ark_pid=ark_pid)

            articles_info = variables.sparql_get_article_object.get_articles()
            articles = []
            # Request all the articles of the project
            articles_project = variables.sparql_get_project_object.get_articles_project(ark_pid)
            for basic_info_article in articles_info:
                if not (basic_info_article[0] in [article[0] for article in articles_project]):
                    articles.append(
                        '''{}, {}'''.format(basic_info_article[1], basic_info_article[0]))

            context = {
                'button_value': 'Ajouter',
                'title_data_type_added': 'Article',
                'data_type_added': 'de l\'article',
                'url_to_return': '/projects/edition/field/add-article/{}'.format(ark_pid),
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


def project_article_deletion(request, ark_pid):
    '''
    Deletes an article of the given project

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = variables.sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:
            article = request.POST.get('articleARK', '')
            variables.sparql_post_project_object.delete_article_of_project(ark_pid, article)

            return redirect(project_edition, ark_pid=ark_pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def project_deletion(request, ark_pid):
    '''
    Deletes completely an project and all his leafs

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
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
        members_project = variables.sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:
            variables.sparql_generic_post_object.delete_subject(ark_pid)
            variables.sparql_generic_post_object.delete_subject(ark_pid+"ARK")

            return redirect(views.index)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet projet",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet projet"
    }
    return render(request, 'page_info.html', context)
