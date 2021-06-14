from django.shortcuts import render, redirect
from .forms import *
import re
import string
from arketype_API.ark import Ark
from sparql_triplestore.sparql_requests.sparql_generic_post_methods import SparqlGenericPostMethods
from sparql_triplestore.sparql_requests.person.sparql_get_Person_methods import SparqlGetPersonMethods
from sparql_triplestore.sparql_requests.articles.sparql_get_articles_methods import SparqlGetArticlesMethods
from sparql_triplestore.sparql_requests.articles.sparql_post_articles_methods import SparqlPostArticlesMethods
from sparql_triplestore.sparql_requests.projects.sparql_get_projects_methods import SparqlGetProjectsMethods
from sparql_triplestore.sparql_requests.projects.sparql_post_projects_methods import SparqlPostProjectsMethods

sparql_generic_post_object = SparqlGenericPostMethods()
sparql_get_person_object = SparqlGetPersonMethods()
sparql_get_article_object = SparqlGetArticlesMethods()
sparql_post_article_object = SparqlPostArticlesMethods()
sparql_get_project_object = SparqlGetProjectsMethods()
sparql_post_project_object = SparqlPostProjectsMethods()


def project_results(request):
    alphabet_list = list(string.ascii_lowercase)
    categories = ["Projets de recherche"]
    category = categories[0]
    sparql_request = sparql_get_project_object.get_projects()
    context = {
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
    }

    return render(request, 'project/project_results.html', context)


def project_creation(request):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Check the request method
        if request.method == 'POST':
            form = ProjectCreationForm(request.POST)
            if form.is_valid():
                members = re.findall('"([^"]*)"', request.POST['memberElementsPost'])
                print(members)
                ark_pid = form.cleaned_data['ark_pid']
                if ark_pid == '':
                    ark_pid = Ark().ark_creation()
                sparql_post_project_object.create_project(ark_pid, form.cleaned_data['name'],
                                                          form.cleaned_data['description'],
                                                          form.cleaned_data['founding_date'], form.cleaned_data['dissolution_date'], form.cleaned_data['url'])
                for member in members:
                    sparql_post_project_object.add_member_to_project(ark_pid, member.split()[-1])
                return redirect(index)
        else:
            form = ProjectCreationForm()
        persons_info = sparql_get_person_object.get_persons()
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
    # Verify in triplestore if the ark_pid correspond to a project
    sparql_request_check_project_ark = sparql_get_project_object.check_project_ark(ark_pid)
    print(ark_pid)
    if sparql_request_check_project_ark:
        data_project = sparql_get_project_object.get_data_project(ark_pid)
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
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:
            edition_granted = True
            data_project = sparql_get_project_object.get_data_project(ark_pid)
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


def project_deletion(request, ark_pid):
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:
            sparql_post_project_object.delete_project(ark_pid)

            return redirect(index)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet projet",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet projet"
    }
    return render(request, 'page_info.html', context)
