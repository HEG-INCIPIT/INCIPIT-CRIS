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


def index(request):
    '''
    Show Visualizer
    '''
    context = {
    }
    return render(request, 'visualizer/index.html', context)
