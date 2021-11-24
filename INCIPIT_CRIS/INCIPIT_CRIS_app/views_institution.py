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


def institution_results(request):
    '''
    Search in the triplestore all the institutions and format a dictionnary that's used
    in the template to display information.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display results for institutions and a dictionnary with all the data needed to fulfill
        the template.
    '''

    alphabet_list = list(string.ascii_lowercase)
    categories = ['Institutions']
    category = categories[0]
    sparql_request = variables.sparql_get_institution_object.get_institutions()
    context = {
        'path_name' : ['Institutions'],
        'path_url' : ['/institutions/'],
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
        'url':'/institutions/',
    }

    return render(request, 'generic/organization_results.html', context)


def institution_creation(request):
    '''
    Create a institution in the triplestore and mint an ARK if it's not given

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
            form = InstitutionCreationForm(request.POST)
            if form.is_valid():
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
                variables.sparql_post_institution_object.create_institution(pid, form.cleaned_data['name'],
                                                        form.cleaned_data['alternate_name'],
                                                        form.cleaned_data['description'],
                                                        form.cleaned_data['founding_date'], form.cleaned_data['url'], form.cleaned_data['url_logo'], request.POST['institutions'])

                if 'funder' in list(request.POST.keys()) and request.POST['funder'] == 'on':
                    variables.sparql_post_funder_object.define_institution_funder(pid)

                return redirect(views.index)
        else:
            form = InstitutionCreationForm()

        top_lvl_institutions = variables.sparql_get_institution_object.get_top_lvl_institutions()
        top_lvl_institutions_data = []
        for top_lvl_institution in top_lvl_institutions:
            top_lvl_institutions_data.append(variables.sparql_get_institution_object.get_dict_institution(top_lvl_institution[0]))

        context = {
            'form': form,
            'button_value': 'Créer',
            'url_to_return': '/institutions/creation/',
            'institutions': json.dumps(top_lvl_institutions_data),
        }
        # return the form to be completed
        return render(request, 'forms/institution/institution_creation.html', context)

    else:
        context = {
            'message': "Connectez-vous pour pourvoir créer des projets"
        }

        return render(request, 'page_info.html', context)


def institution_profile(request, pid):
    '''
    Display a page with all the data of a institution that is given by the pid.

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

    # Verify in triplestore if the pid correspond to a institution
    sparql_request_check_institution_ark = variables.sparql_get_institution_object.check_institution_ark(pid)
    if sparql_request_check_institution_ark:
        data_institution = variables.sparql_get_institution_object.get_data_institution(pid)
        can_edit = True if request.user.is_authenticated and request.user.is_superuser else False
        edition_granted = False
        if request.user.is_superuser:
            edition_granted = True
        context = {
            'can_edit': can_edit,
            'edition_granted': edition_granted,
            'data_institution': data_institution,
        }
        return render(request, 'institution/institution_profile.html', context)

    return render(request, 'page_404.html')


def institution_edition(request, pid):
    '''
    Display a page with all the data of the institution given by the pid and adds links to modify some parts.

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
        # Verify if the user is admin to grant edition
        if request.user.is_superuser:
            # Request all the data of the given institution
            data_institution = variables.sparql_get_institution_object.get_data_institution(pid)
            context = {
                'data_institution': data_institution
            }
            return render(request, 'institution/institution_profile_edition.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cette institution",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cette institution"
    }
    return render(request, 'page_info.html', context)


def institution_field_edition(request, field_to_modify, pid):
    '''
    Handle the display and the selection of the correct form to modify a given field

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    field_to_modify : String
        Indicates the field that is asked to be modified.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the field of the profil of a institution that is going to be modified and a dictionnary
        with all the data needed to fulfill the template.
    '''

    context = {}
    form = forms.Form()
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify if the user ark is in the institutions members to grant edition
        if request.user.is_superuser:

            data_institution = variables.sparql_get_institution_object.get_data_institution(pid)
            form = form_selection.form_selection(request, field_to_modify, data_institution)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    if field_to_modify == 'foundingDate':
                        date_institution = str(data_institution['modified_date']) + " 00:00:00+00:00" if data_institution['modified_date'] != 'None' else str(data_institution['modified_date'])
                        variables.sparql_generic_post_object.update_date_leaf(pid, field_to_modify,
                                                                    form.cleaned_data['founding_date'],
                                                                    date_institution)
                    elif field_to_modify == 'alternateName':
                        variables.sparql_generic_post_object.update_string_leaf(pid, field_to_modify,
                                                                      form.cleaned_data['alternate_name'],
                                                                      data_institution['alternate_name'])
                    elif field_to_modify == 'logo':
                        variables.sparql_generic_post_object.update_string_leaf(pid, field_to_modify,
                                                                      form.cleaned_data['url'],
                                                                      data_institution[field_to_modify])
                    else:
                        variables.sparql_generic_post_object.update_string_leaf(pid, field_to_modify,
                                                                      form.cleaned_data[field_to_modify],
                                                                      data_institution[field_to_modify])
                    return redirect(institution_edition, pid=pid)

            context = {
                'form': form,
                'path_name' : ['Institution', 'Profil', 'Edition', form.fields[next(iter(form.declared_fields.keys()))].label],
                'path_url' : ['/institutions/', '/institutions/'+pid, '/institutions/edition/'+pid, '/institutions/edition/field/'+field_to_modify+pid],
                'button_value': 'Modifier',
                'url_to_return': '/institutions/edition/field/{}/{}'.format(field_to_modify, pid)
            }
            # return the form to be completed
            return render(request, 'forms/classic_form.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet institution",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet institution"
    }
    return render(request, 'page_info.html', context)


def institution_parent_organization_addition(request, pid):
    '''
    Adds a parent organization to an organization

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
        # Verify that the edition of profile is made by the admin
        if request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                organization = request.POST['institutions']
                if organization != '':
                    variables.sparql_post_institution_object.add_parent_institution_to_institution(pid, organization)

                return redirect(institution_edition, pid=pid)

            top_lvl_institutions = variables.sparql_get_institution_object.get_top_lvl_institutions()
            top_lvl_institutions_data = []
            for top_lvl_institution in top_lvl_institutions:
                top_lvl_institutions_data.append(variables.sparql_get_institution_object.get_dict_institution(top_lvl_institution[0]))

            context = {
                'path_name' : ['Institutions', 'Profil', 'Edition', 'Ajouter une institution parente'],
                'path_url' : ['/institutions/', '/institutions/'+pid, '/institutions/edition/'+pid, '/institutions/edition/field/add-parent-institution/'+pid],
                'title_data_type_added': 'Institution parente',
                'data_type_added': 'de l\'institution parente',
                'url_to_return': '/institutions/edition/field/add-parent-institution/{}'.format(pid),
                'button_value': 'Ajouter',
                'institutions': json.dumps(top_lvl_institutions_data),
            }

            return render(request, 'forms/select_institution_form.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cette institution",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cette institution"
    }
    return render(request, 'page_info.html', context)


def institution_parent_organization_deletion(request, pid):
    '''
    Deletes a parent institution of the given institution

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a institution.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the admin
        if request.user.is_superuser:
            institution = request.POST.get('institutionARK', '')
            variables.sparql_post_institution_object.delete_parent_institution_to_institution(pid, institution)

            return redirect(institution_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cette institution",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cette institution"
    }
    return render(request, 'page_info.html', context)


def institution_sub_organization_addition(request, pid):
    '''
    Adds a sub organization to an organization

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
        # Verify that the edition of profile is made by the admin
        if request.user.is_superuser:

            # Check the request method
            if request.method == 'POST':
                organization = request.POST['institutions']
                if organization != '':
                    variables.sparql_post_institution_object.add_sub_institution_to_institution(pid, organization)

                return redirect(institution_edition, pid=pid)

            top_lvl_institutions = variables.sparql_get_institution_object.get_top_lvl_institutions()
            top_lvl_institutions_data = []
            for top_lvl_institution in top_lvl_institutions:
                top_lvl_institutions_data.append(variables.sparql_get_institution_object.get_dict_institution(top_lvl_institution[0]))

            context = {
                'path_name' : ['Institutions', 'Profil', 'Edition', 'Ajouter une institution sube'],
                'path_url' : ['/institutions/', '/institutions/'+pid, '/institutions/edition/'+pid, '/institutions/edition/field/add-sub-institution/'+pid],
                'title_data_type_added': 'Sous-institution',
                'data_type_added': 'de l\'sous-institution',
                'url_to_return': '/institutions/edition/field/add-sub-institution/{}'.format(pid),
                'button_value': 'Ajouter',
                'institutions': json.dumps(top_lvl_institutions_data),
            }

            return render(request, 'forms/select_institution_form.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cette institution",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cette institution"
    }
    return render(request, 'page_info.html', context)


def institution_sub_organization_deletion(request, pid):
    '''
    Deletes a sub institution of the given institution

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a institution.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the admin
        if request.user.is_superuser:
            institution = request.POST.get('institutionARK', '')
            variables.sparql_post_institution_object.delete_sub_institution_to_institution(pid, institution)

            return redirect(institution_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cette institution",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cette institution"
    }
    return render(request, 'page_info.html', context)


def institution_worker_addition(request, pid):
    '''
    Adds an organisation where the given institution works

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
                workers = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for worker in workers:
                    variables.sparql_post_person_object.add_work_person(worker.split()[-1], pid)

                return redirect(institution_edition, pid=pid)

            persons = []

            workers_institution = variables.sparql_get_institution_object.get_workers_institution(pid)

            # Request all the persons in the triplestore
            persons_info = variables.sparql_get_person_object.get_persons()
            for basic_info_person in persons_info:
                if not (basic_info_person[0] in [worker['pid'] for worker in workers_institution]):
                    persons.append(
                        '''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))

            context = {
                'path_name' : ['Institutions', 'Profil', 'Edition', 'Ajouter un employé'],
                'path_url' : ['/institutions/', '/institutions/'+pid, '/institutions/edition/'+pid, '/institutions/edition/field/add-worker/'+pid],
                'title_data_type_added': 'Employé(s)',
                'data_type_added': 'de l\'employé',
                'url_to_return': '/institutions/edition/field/add-worker/{}'.format(pid),
                'button_value': 'Ajouter',
                'data': persons,
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


def institution_worker_deletion(request, pid):
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
            worker = request.POST.get('workerARK', '')
            variables.sparql_post_person_object.delete_work_person(worker, pid)

            return redirect(institution_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def institution_affiliate_addition(request, pid):
    '''
    Adds an organisation where the given institution affiliations

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
                affiliates = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for affiliate in affiliates:
                    variables.sparql_post_person_object.add_affiliation_person(affiliate.split()[-1], pid)

                return redirect(institution_edition, pid=pid)

            persons = []

            affiliates_institution = variables.sparql_get_institution_object.get_affiliates_institution(pid)

            # Request all the persons in the triplestore
            persons_info = variables.sparql_get_person_object.get_persons()
            for basic_info_person in persons_info:
                if not (basic_info_person[0] in [affiliate['pid'] for affiliate in affiliates_institution]):
                    persons.append(
                        '''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))

            context = {
                'path_name' : ['Institutions', 'Profil', 'Edition', 'Ajouter un employé'],
                'path_url' : ['/institutions/', '/institutions/'+pid, '/institutions/edition/'+pid, '/institutions/edition/field/add-affiliate/'+pid],
                'title_data_type_added': 'Employé(s)',
                'data_type_added': 'de l\'employé',
                'url_to_return': '/institutions/edition/field/add-affiliate/{}'.format(pid),
                'button_value': 'Ajouter',
                'data': persons,
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


def institution_affiliate_deletion(request, pid):
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
            affiliate = request.POST.get('affiliateARK', '')
            variables.sparql_post_person_object.delete_affiliation_person(affiliate, pid)

            return redirect(institution_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def institution_article_addition(request, pid):
    '''
    Adds an organisation where the given institution articles

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
                articles = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for article in articles:
                    variables.sparql_post_article_object.add_institution_to_article(article.split()[-1], pid)

                return redirect(institution_edition, pid=pid)

            articles = []

            articles_institution = variables.sparql_get_institution_object.get_articles_institution(pid)

            # Request all the articles in the triplestore
            articles_info = variables.sparql_get_article_object.get_articles()
            for basic_info_article in articles_info:
                if not (basic_info_article[0] in [article['pid'] for article in articles_institution]):
                    articles.append(
                        '''{}, {}'''.format(basic_info_article[1], basic_info_article[0]))

            context = {
                'path_name' : ['Institutions', 'Profil', 'Edition', 'Ajouter un article'],
                'path_url' : ['/institutions/', '/institutions/'+pid, '/institutions/edition/'+pid, '/institutions/edition/field/add-article/'+pid],
                'title_data_type_added': 'Article(s)',
                'data_type_added': 'de l\'article',
                'url_to_return': '/institutions/edition/field/add-article/{}'.format(pid),
                'button_value': 'Ajouter',
                'data': articles,
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


def institution_article_deletion(request, pid):
    '''
    Edit an organisation where the given article articles

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a article.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Get the value of a variable in the POST request by its id
            article = request.POST.get('articleARK', '')
            variables.sparql_post_article_object.delete_institution_from_article(article, pid)

            return redirect(institution_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def institution_project_addition(request, pid):
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
                    variables.sparql_post_project_object.add_institution_to_project(project.split()[-1], pid)

                return redirect(institution_edition, pid=pid)

            projects = []

            projects_institution = variables.sparql_get_institution_object.get_projects_institution(pid)

            # Request all the projects in the triplestore
            projects_info = variables.sparql_get_project_object.get_projects()
            for basic_info_project in projects_info:
                if not (basic_info_project[0] in [project['pid'] for project in projects_institution]):
                    projects.append(
                        '''{}, {}'''.format(basic_info_project[1], basic_info_project[0]))

            context = {
                'path_name' : ['Institutions', 'Profil', 'Edition', 'Ajouter un project'],
                'path_url' : ['/institutions/', '/institutions/'+pid, '/institutions/edition/'+pid, '/institutions/edition/field/add-project/'+pid],
                'title_data_type_added': 'Projet(s)',
                'data_type_added': 'du projet',
                'url_to_return': '/institutions/edition/field/add-project/{}'.format(pid),
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


def institution_project_deletion(request, pid):
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
            project = request.POST.get('projectARK', '')
            variables.sparql_post_project_object.delete_institution_from_project(project, pid)

            return redirect(institution_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def institution_dataset_addition(request, pid):
    '''
    Adds an organisation where the given institution datasets

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
                datasets = re.findall('"([^"]*)"', request.POST['groupElementsPost'])
                for dataset in datasets:
                    variables.sparql_post_dataset_object.add_institution_to_dataset(dataset.split()[-1], pid)

                return redirect(institution_edition, pid=pid)

            datasets = []

            datasets_institution = variables.sparql_get_institution_object.get_datasets_institution(pid)

            # Request all the datasets in the triplestore
            datasets_info = variables.sparql_get_dataset_object.get_datasets()
            for basic_info_dataset in datasets_info:
                if not (basic_info_dataset[0] in [dataset['pid'] for dataset in datasets_institution]):
                    datasets.append(
                        '''{}, {}'''.format(basic_info_dataset[1], basic_info_dataset[0]))

            context = {
                'path_name' : ['Institutions', 'Profil', 'Edition', 'Ajouter un dataset'],
                'path_url' : ['/institutions/', '/institutions/'+pid, '/institutions/edition/'+pid, '/institutions/edition/field/add-dataset/'+pid],
                'title_data_type_added': 'Projet(s)',
                'data_type_added': 'du projet',
                'url_to_return': '/institutions/edition/field/add-dataset/{}'.format(pid),
                'button_value': 'Ajouter',
                'data': datasets,
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


def institution_dataset_deletion(request, pid):
    '''
    Edit an organisation where the given dataset datasets

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
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            # Get the value of a variable in the POST request by its id
            dataset = request.POST.get('datasetARK', '')
            variables.sparql_post_dataset_object.delete_institution_from_dataset(dataset, pid)

            return redirect(institution_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def institution_funder_addition(request, pid):
    '''
    Edit an organisation where the given funder funders

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a funder.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            if request.method == 'POST':
                variables.sparql_post_funder_object.define_institution_funder(pid)

            return redirect(institution_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def institution_funder_deletion(request, pid):
    '''
    Edit an organisation where the given funder funders

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    pid: String
        It's a string representing the PID of the current object.

    Returns
    -------
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page of edition of a funder.
    '''

    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.pid == pid or request.user.is_superuser:

            if request.method == 'POST':
                variables.sparql_post_funder_object.delete_institution_funder(pid)

            return redirect(institution_edition, pid=pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer ce profil",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer ce profil"
    }
    return render(request, 'page_info.html', context)


def institution_deletion(request, pid):
    '''
    Deletes the given institution

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

    # Verify that the user is authenticated
    if request.user.is_authenticated:
        # Verify if the user is admin to grant deletion
        if request.user.is_superuser:

            variables.sparql_generic_post_object.delete_subject(pid)
            variables.sparql_generic_post_object.delete_object(pid)
            variables.sparql_generic_post_object.delete_subject(pid+"ARK")
            variables.sparql_generic_post_object.delete_object(pid+"ARK")

            return redirect(views.index)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cette institution",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cette institution"
    }
    return render(request, 'page_info.html', context)
