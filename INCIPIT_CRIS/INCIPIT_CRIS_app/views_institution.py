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

    return render(request, 'generic/results.html', context)


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
                        pid = variables.ark.mint(form.cleaned_data['url'], '{} {}'.format(request.user.first_name, request.user.last_name), 
                            form.cleaned_data['name'], form.cleaned_data['founding_date'])
                    except:
                        raise Exception
                variables.sparql_post_institution_object.create_institution(pid, form.cleaned_data['name'],
                                                        form.cleaned_data['alternate_name'],
                                                        form.cleaned_data['description'],
                                                        form.cleaned_data['founding_date'], form.cleaned_data['url'], request.POST['institutions'])
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
        edition_granted = False
        if request.user.is_superuser or request.user.is_authenticated and request.user.pid in [members[0] for members in data_institution['members']]:
            edition_granted = True
        context = {
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
        # Request all the members of the institution
        members_institution = variables.sparql_get_institution_object.get_members_institution(pid)
        # Verify if the user ark is in the institutions members to grant edition
        if request.user.pid in [members[0] for members in members_institution] or request.user.is_superuser:

            data_institution = variables.sparql_get_institution_object.get_data_institution(pid)

            form = form_selection.form_selection(request, field_to_modify, data_institution)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    if field_to_modify == 'foundingDate':
                        variables.sparql_generic_post_object.update_date_leaf(pid, field_to_modify,
                                                                    form.cleaned_data['founding_date'],
                                                                    str(data_institution['founding_date']) +
                                                                    " 00:00:00+00:00")
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
