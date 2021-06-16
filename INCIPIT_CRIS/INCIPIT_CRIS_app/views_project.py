from django.shortcuts import render, redirect
from .forms import *
import re
import string
from . import views
from . import variables


def project_results(request):
    alphabet_list = list(string.ascii_lowercase)
    categories = ["Projets de recherche"]
    category = categories[0]
    sparql_request = variables.sparql_get_project_object.get_projects()
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
                ark_pid = form.cleaned_data['ark_pid']
                if ark_pid == '':
                    ark_pid = variables.Ark().ark_creation()
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


def project_field_edition(request, part_of_project_to_edit, ark_pid):
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
                    variables.sparql_post_project_object.add_member_to_project(ark_pid, member.split()[2])

                return redirect(project_edition, ark_pid=ark_pid)

            persons_info = variables.sparql_get_person_object.get_persons()
            persons = []
            for basic_info_person in persons_info:
                if not (basic_info_person[0] in [member[0] for member in members_project]):
                    persons.append(
                        '''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))

            context = {
                'button_value': 'Ajouter',
                'title_of_person_added': 'Membre',
                'url_to_return': '/projects/edition/field/add-member/{}'.format(ark_pid),
                'persons': persons
            }
            # return the form to be completed
            return render(request, 'forms/add_person_to_group.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)


def project_member_deletion(request, ark_pid):
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


def project_deletion(request, ark_pid):
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
