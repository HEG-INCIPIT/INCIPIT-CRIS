from django.shortcuts import render, redirect
from .forms import *
import re
import string
import datetime
from django.conf import settings
from . import views
from . import variables


def dataset_results(request):
    '''
    Search in the triplestore all the datasets and format a dictionnary that's used
    in the template to display information.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display results for datasets and a dictionnary with all the data needed to fulfill
        the template.
    '''
    alphabet_list = list(string.ascii_lowercase)
    categories = ['Jeux de données']
    category = categories[0]
    sparql_request = variables.sparql_get_dataset_object.get_datasets()
    context = {
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
        'url':'/datasets/'
    }

    return render(request, 'generic/results.html', context)


def dataset_creation(request):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Check the request method
        if request.method == 'POST':
            form = DatasetCreationForm(request.POST)
            if form.is_valid():
                maintainer = re.findall('"([^"]*)"', request.POST['maintainerElementsPost'])
                ark_pid = form.cleaned_data['ark_pid']
                if ark_pid == '':
                    try:
                        ark_pid = variables.ark.mint('', '{}'.format(form.cleaned_data['name']), 
                            'Creating an ARK in INCIPIT-CRIS for a dataset named {}'.format(form.cleaned_data['name']), '{}'.format(datetime.datetime.now()))
                        variables.ark.update('{}'.format(ark_pid), '{}{}'.format(settings.URL, ark_pid), '{} {}'.format(form.cleaned_data['name']), 
                            'Creating an ARK in INCIPIT-CRIS for a dataset named {}'.format(form.cleaned_data['name']), '{}'.format(datetime.datetime.now()))
                    except:
                        print("ERROR")
                        raise Exception
                variables.sparql_post_dataset_object.create_dataset(ark_pid, form.cleaned_data['name'],
                                                          form.cleaned_data['abstract'],
                                                          form.cleaned_data['date_published'], form.cleaned_data['url'])
                for maintainer in maintainer:
                    variables.sparql_post_dataset_object.add_maintainer_to_dataset(ark_pid, maintainer.split()[-1])
                return redirect(views.index)
        else:
            form = DatasetCreationForm()
        persons_info = variables.sparql_get_person_object.get_persons()
        persons = []
        for basic_info_person in persons_info:
            persons.append('''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))
        context = {
            'form': form,
            'button_value': 'Créer',
            'url_to_return': '/datasets/creation/',
            'persons': persons
        }
        # return the form to be completed
        return render(request, 'forms/dataset/dataset_creation.html', context)

    else:
        context = {
            'message': "Connectez-vous pour pourvoir créer des datasets"
        }

        return render(request, 'page_info.html', context)