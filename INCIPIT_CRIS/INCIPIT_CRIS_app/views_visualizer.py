from SPARQLWrapper.Wrapper import ADD
from django.shortcuts import redirect, render
from .forms import *
from . import variables
from django.core.files.storage import FileSystemStorage
from os import listdir, remove, path
from os.path import isfile, join
from django.conf import settings
from random import sample
import requests
import socket

def index(request):
    '''
    Show Visualizer

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HTTPResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''
    context = {
        "ip": socket.gethostbyname(socket.gethostname())
    }
    return render(request, 'visualizer/index.html', context)
