from django.shortcuts import render, redirect
from .forms import *
import re
import string
import datetime
from django.conf import settings
from . import views
from . import variables
from . import form_selection
import json
from .views_institution import institution_edition


def funder_results(request):
    '''
    Search in the triplestore all the funders and format a dictionnary that's used
    in the template to display information.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display results for funders and a dictionnary with all the data needed to fulfill
        the template.
    '''

    alphabet_list = list(string.ascii_lowercase)
    categories = ['Bailleurs de fond']
    category = categories[0]
    sparql_request = variables.sparql_get_funder_object.get_funders()
    context = {
        'path_name' : ['Bailleurs de fond'],
        'path_url' : ['/funders/'],
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
        'url':'/institutions/',
    }

    return render(request, 'generic/organization_results.html', context)


def funder_project_addition(request, pid):
    '''
    Adds an organisation where the given institution projects

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a institution.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                projects = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for project in projects:
                    variables.sparql_post_funder_object.add_project_to_funder(pid, project.split()[-1])

                return redirect(institution_edition, pid=pid)

            projects = []

            projects_institution = variables.sparql_get_funder_object.get_projects_funder(pid)

            # Request all the projects in the triplestore
            projects_info = variables.sparql_get_project_object.get_projects()
            for basic_info_project in projects_info:
                if not (basic_info_project[0] in [project['pid'] for project in projects_institution]):
                    projects.append(
                        '''{}, {}'''.format(basic_info_project[1], basic_info_project[0]))

            context = {
                'path_name' : ['Bailleur de fonds', 'Profil', 'Edition', 'Ajouter un project'],
                'path_url' : ['/funders/', '/funders/'+pid, '/funders/edition/'+pid, '/funders/edition/field/add-project/'+pid],
                'title_data_type_added': 'Projet(s)',
                'data_type_added': 'du projet',
                'url_to_return': '/funders/edition/field/add-project/{}'.format(pid),
                'button_value': 'Ajouter',
                'data': projects,
            }

            return render(request, 'forms/autocompletion_group.html', context)
    
        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def funder_project_deletion(request, pid):
    '''
    Edit an organisation where the given project projects

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a project.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Get the value of a variable in the POST request by its id
            project = request.POST.get('project_fundedARK', '')
            variables.sparql_post_funder_object.delete_project_from_funder(pid, project)

            return redirect(institution_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)
