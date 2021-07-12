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
    '''
    Create in the triplestore a dataset from the data provided from the form requested

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
    HttpResponseRedirect
        A HttpResponseRedirect object that redirect to the page to create a dataset.
    '''

    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Check the request method
        if request.method == 'POST':
            form = DatasetCreationForm(request.POST)
            if form.is_valid():
                maintainers = re.findall('"([^"]*)"', request.POST['maintainerElementsPost'])
                print("\n")
                print(maintainers)
                creators = re.findall('"([^"]*)"', request.POST['creatorElementsPost'])
                print(creators)
                print("\n")
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
                                                          form.cleaned_data['created_date'], 
                                                          form.cleaned_data['modified_date'], 
                                                          form.cleaned_data['url_data'], 
                                                          form.cleaned_data['url_details'])
                for maintainer in maintainers:
                    variables.sparql_post_dataset_object.add_maintainer_to_dataset(ark_pid, maintainer.split()[-1])
                for creator in creators:
                    variables.sparql_post_dataset_object.add_creator_to_dataset(ark_pid, creator.split()[-1])
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


def dataset_profile(request, ark_pid):
    '''
    Display a page with all the data of a dataset that is given by the ark_pid.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display and a dictionnary with all the data needed to fulfill the template.
    '''

    # Verify in triplestore if the ark_pid correspond to a dataset
    sparql_request_check_dataset_ark = variables.sparql_get_dataset_object.check_dataset_ark(ark_pid)
    if sparql_request_check_dataset_ark:
        data_dataset = variables.sparql_get_dataset_object.get_data_dataset(ark_pid)
        edition_granted = False
        if request.user.is_authenticated and (request.user.ark_pid in [maintainer[0] for maintainer in data_dataset['maintainers']] or request.user.ark_pid in [creator[0] for creator in data_dataset['creators']]):
            edition_granted = True
        context = {
            'edition_granted': edition_granted,
            'data_dataset': data_dataset
        }
        print(data_dataset)
        return render(request, 'dataset/dataset_profile.html', context)

    return render(request, 'page_404.html')


def dataset_edition(request, ark_pid):
    '''
    Display a page with all the data of the dataset given by the ark_pid and adds links to modify some parts.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    ark_pid: String
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
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(ark_pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(ark_pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.ark_pid in [creators[0] for creators in creators_dataset] or request.user.ark_pid in [maintainers[0] for maintainers in maintainers_dataset] or request.user.is_superuser:
            edition_granted = True
            data_dataset = variables.sparql_get_dataset_object.get_data_dataset(ark_pid)
            context = {
                'edition_granted': edition_granted,
                'data_dataset': data_dataset
            }
            return render(request, 'dataset/dataset_profile_edition.html', context)

        edition_granted = False
        context = {
            'message': "Vous n'avez pas le droit d'éditer cet dataset",
            'edition_granted': edition_granted
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_form_selection(request, part_of_dataset_to_edit, data_dataset):
    '''
    Select and return the correct form to be used in order to modify a field.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    part_of_dataset_to_modify : String
        Indicates the field that is asked to be modified.
    data_dataset : Dictionary
        Contain the data of the different fields of a dataset.

    Returns
    -------
    Form
        A form with the fields desired
    '''

    # Check the request method
    if request.method == 'POST':
        if part_of_dataset_to_edit == 'name':
            return NameForm(request.POST)
        if part_of_dataset_to_edit == 'abstract':
            return AbstractForm(request.POST)
        if part_of_dataset_to_edit == 'dateCreated':
            return DatasetCreatedDateForm(request.POST)
        if part_of_dataset_to_edit == 'dateModified':
            return DatasetModifiedDateForm(request.POST)
        if part_of_dataset_to_edit == 'urlDetails':
            return DatasetURLDetailsForm(request.POST)
        if part_of_dataset_to_edit == 'urlData':
            return DatasetURLDataForm(request.POST)

    # if not a POST it'll create a blank form
    else:
        if part_of_dataset_to_edit == 'name':
            return NameForm(old_name=data_dataset[part_of_dataset_to_edit])
        if part_of_dataset_to_edit == 'abstract':
            return AbstractForm(old_abstract=data_dataset[part_of_dataset_to_edit])
        if part_of_dataset_to_edit == 'dateCreated':
            return DatasetCreatedDateForm(old_created_date=data_dataset['created_date'])
        if part_of_dataset_to_edit == 'dateModified':
            return DatasetModifiedDateForm(old_modified_date=data_dataset['modified_date'])
        if part_of_dataset_to_edit == 'urlDetails':
            return DatasetURLDetailsForm(old_url_details=data_dataset['url_details'])
        if part_of_dataset_to_edit == 'urlData':
            return DatasetURLDataForm(old_url_data=data_dataset['url_data']['url_data'])



def dataset_field_edition(request, part_of_dataset_to_edit, ark_pid):
    '''
    Handle the display and the selection of the correct form to modify a given field

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    part_of_article_to_modify : String
        Indicates the field that is asked to be modified.
    ark_pid: String
        It's a string representing an ARK.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the field of the profil of a dataset that is going to be modified and a dictionnary
        with all the data needed to fulfill the template.
    '''
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(ark_pid)
        # Request all the maintainers of the dataset
        maintainers_dataset = variables.sparql_get_dataset_object.get_maintainers_dataset(ark_pid)
        # Verify if the user ark is in the datasets creators or maintainers to grant edition
        if request.user.ark_pid in [creators[0] for creators in creators_dataset] or request.user.ark_pid in [maintainers[0] for maintainers in maintainers_dataset] or request.user.is_superuser:

            data_dataset = variables.sparql_get_dataset_object.get_data_dataset(ark_pid)

            form = dataset_form_selection(request, part_of_dataset_to_edit, data_dataset)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    if part_of_dataset_to_edit == 'dateCreated':
                        variables.sparql_generic_post_object.update_date_leaf(ark_pid, part_of_dataset_to_edit,
                                                                    form.cleaned_data['created_date'],
                                                                    str(data_dataset['created_date']) +
                                                                    ' 00:00:00+00:00')
                    elif part_of_dataset_to_edit == 'dateModified':
                        variables.sparql_generic_post_object.update_date_leaf(ark_pid, part_of_dataset_to_edit,
                                                                    form.cleaned_data['modified_date'],
                                                                    str(data_dataset['modified_date']) +
                                                                    ' 00:00:00+00:00')
                    elif part_of_dataset_to_edit == 'urlDetails':
                        variables.sparql_generic_post_object.update_string_leaf(ark_pid, 'url',
                                                                    form.cleaned_data['url_details'],
                                                                    data_dataset['url_details'])
                    elif part_of_dataset_to_edit == 'urlData':
                        variables.sparql_generic_post_object.update_string_leaf(str(ark_pid)+'DD', 'url',
                                                                    form.cleaned_data['url_data'],
                                                                    data_dataset['url_data']['url_data'])
                    else:
                        variables.sparql_generic_post_object.update_string_leaf(ark_pid, part_of_dataset_to_edit,
                                                                      form.cleaned_data[part_of_dataset_to_edit],
                                                                      data_dataset[part_of_dataset_to_edit])
                    return redirect(dataset_edition, ark_pid=ark_pid)

            context = {
                'form': form,
                'button_value': 'Modifier',
                'url_to_return': '/datasets/edition/field/{}/{}'.format(part_of_dataset_to_edit, ark_pid)
            }
            # return the form to be completed
            return render(request, 'forms/classic_form.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet dataset"
    }
    return render(request, 'page_info.html', context)


def dataset_deletion(request, ark_pid):
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the creators of the dataset
        creators_dataset = variables.sparql_get_dataset_object.get_creators_dataset(ark_pid)
        # Verify if the user ark is in the datasets creators to grant edition
        if request.user.ark_pid in [creators[0] for creators in creators_dataset] or request.user.is_superuser:
            variables.sparql_generic_post_object.delete_subject(ark_pid)
            variables.sparql_generic_post_object.delete_subject(ark_pid+"ARK")
            variables.sparql_generic_post_object.delete_subject(ark_pid+"DD")

            return redirect(views.index)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet dataset",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet dataset"
    }
    return render(request, 'page_info.html', context)
