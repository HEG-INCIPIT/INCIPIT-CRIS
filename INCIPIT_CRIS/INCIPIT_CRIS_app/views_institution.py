from django.shortcuts import render, redirect
from .forms import *
import re
import string
import datetime
from django.conf import settings
from . import views
from . import variables
from . import form_selection


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
    categories = ['Institutions', 'HEG', 'UNIGE', 'HEdS', 'HEPIA', 'HETS']
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
