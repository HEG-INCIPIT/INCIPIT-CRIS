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
            'data_institution': data_institution
        }
        return render(request, 'institution/institution_profile.html', context)

    return render(request, 'page_404.html')
