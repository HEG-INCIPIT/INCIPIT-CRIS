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