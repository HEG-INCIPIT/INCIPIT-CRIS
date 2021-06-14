from django.shortcuts import render, redirect
from .forms import *
import string
from . import variables


def person_results(request):
    """
    Compute a research of all persons in triplestore for the template
    :param request:
    :return: render function with template and data
    """
    alphabet_list = list(string.ascii_lowercase)
    categories = ["Personnes", "Professeurs ordinaire", "Assistants HES"]
    category = categories[0]
    sparql_request = variables.sparql_get_person_object.get_persons()
    context = {
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
    }

    return render(request, 'person/person_results.html', context)


def person_profile(request, ark_pid):
    """
    Display a page with all the data of the person given by the ark_pid
    :param request: object
    :param ark_pid: string -> Person identifier
    :return: render function with template and data
    """
    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = variables.sparql_get_person_object.check_person_ark(ark_pid)
    can_edit = True if request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser) else False
    if sparql_request_check_person_ark:
        data_person = variables.sparql_get_person_object.get_data_person(ark_pid)
        context = {
            'data_person': data_person,
            'can_edit': can_edit,
            'ark_pid': ark_pid,
        }
        return render(request, 'person/person_profile.html', context)

    return render(request, 'page_404.html')


def person_edition(request, ark_pid):
    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = variables.sparql_get_person_object.check_person_ark(ark_pid)
    if sparql_request_check_person_ark:
        if request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser):
            data_person = variables.sparql_get_person_object.get_data_person(ark_pid)
            context = {
                'data_person': data_person,
                'ark_pid': ark_pid
            }
            return render(request, 'person/person_profile_edition.html', context)
        else:
            if request.user.is_authenticated:
                context = {
                    'message': "Vous n'avez pas le droit d'éditer ce profil"
                }
            else:
                context = {
                    'message': "Connectez-vous pour modifier votre profil"
                }
        return render(request, 'page_info.html', context)

    return render(request, 'page_404.html')


def person_form_selection(request, part_of_person_to_modify, data_person):
    # Check the request method
    if request.method == 'POST':
        if part_of_person_to_modify == 'description':
            return DescriptionForm(request.POST)
        if part_of_person_to_modify == 'telephone':
            return TelephoneForm(request.POST)

    # if not a POST it'll create a blank form
    else:
        if part_of_person_to_modify == 'description':
            return DescriptionForm(old_description=data_person[part_of_person_to_modify])
        if part_of_person_to_modify == 'telephone':
            return TelephoneForm(old_telephone=data_person[part_of_person_to_modify])


def person_field_edition(request, part_of_person_to_modify, ark_pid):
    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = variables.sparql_get_person_object.check_person_ark(ark_pid)

    if sparql_request_check_person_ark:
        # Verify that the user is authenticated and has the right to modify the profile
        if request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser):

            data_person = variables.sparql_get_person_object.get_data_person(ark_pid)

            form = person_form_selection(request, part_of_person_to_modify, data_person)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    variables.sparql_generic_post_object.update_string_leaf(ark_pid, part_of_person_to_modify,
                                                                  form.cleaned_data[part_of_person_to_modify],
                                                                  data_person[part_of_person_to_modify])
                    return redirect(person_edition, ark_pid=ark_pid)

            context = {
                'form': form,
                'button_value': 'Modifier',
                'url_to_return': '/personnes/edition/profil/{}/{}'.format(part_of_person_to_modify, ark_pid)
            }
            # return the form to be completed
            return render(request, 'forms/person/person_profile_edition.html', context)

        else:
            # Check why the person cannot modify the profile and display the error
            if request.user.is_authenticated:
                context = {
                    'message': "Vous n'avez pas le droit d'éditer ce profil"
                }
            else:
                context = {
                    'message': "Connectez-vous pour modifier votre profil"
                }

        return render(request, 'page_info.html', context)

    return render(request, 'page_404.html')


def person_article_deletion(request, ark_pid):
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Verify that the edition of profile is made by the legitimate user or admin
        if request.user.ark_pid == ark_pid or request.user.is_superuser:
            article = request.POST.get('articleARK', '')
            variables.sparql_post_article_object.delete_author_of_article(article, ark_pid)

            return redirect(person_edition, ark_pid=ark_pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)
