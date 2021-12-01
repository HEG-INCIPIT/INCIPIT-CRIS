from SPARQLWrapper.Wrapper import ADD
from django.shortcuts import redirect, render
from .forms import *
from . import variables
from django.core.files.storage import FileSystemStorage
from os import listdir, remove, path
from os.path import isfile, join
from django.conf import settings
from random import sample
from django.http import HttpResponse
import requests

def search(request):
    '''
    Search data of users from database, articles and project from triplestore and display it all
    in the template

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the index page and a dictionnary with all the data needed to fulfill
        the template.
    '''
    if request.method == 'POST':
        query = request.POST['query']
        return HttpResponse(variables.sparql_post_search_object.search(query))
    else:
        return render(request, "page_error.html", status=405)
