from django.forms.forms import Form
from django.shortcuts import render, redirect
from .forms import DescriptionForm, TelephoneForm
from sparql_triplestore.sparql_requests.person.sparql_get_Person_methods import Sparql_get_Person_methods
from sparql_triplestore.sparql_requests.person.sparql_post_Person_methods import Sparql_post_Person_methods

def index(request):
    return render(request, 'main/index.html')

def persons_research(request):
    sparql_request = Sparql_get_Person_methods().get_persons()
    context = {
        'sparql_request': sparql_request
    }

    return render(request, 'person/display_person_results.html', context)

def person_display(request, ark_pid):
    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = Sparql_get_Person_methods().check_person_ark(ark_pid)
    if(sparql_request_check_person_ark):
        data_person = Sparql_get_Person_methods().get_data_person(ark_pid)
        context = {
            'data_person': data_person
        }
        return render(request, 'person/display_person_profile.html', context)
    
    return render(request, 'page_404.html')

def person_edition_display(request, ark_pid):
    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = Sparql_get_Person_methods().check_person_ark(ark_pid)
    if(sparql_request_check_person_ark):
        if (request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser)):
            data_person = Sparql_get_Person_methods().get_data_person(ark_pid)
            context = {
                'message': "Vous pouvez éditer votre profil",
                'data_person': data_person
            }
            return render(request, 'person/display_person_for_edition.html', context)
        else:
            if(request.user.is_authenticated):
                context = {
                    'message': "Vous n'avez pas le droit d'éditer ce profil"
                }
            else:
                context = {
                    'message': "Connectez-vous pour modifier votre profil"
                }
        return render(request, 'page_info.html', context)
    
    return render(request, 'page_404.html')


def chose_form_to_display(request, part_of_profile_to_modify, data_person):
    # Check the request method
    if (request.method == 'POST'):
        if(part_of_profile_to_modify == 'description'):
            return DescriptionForm(request.POST)
        if(part_of_profile_to_modify == 'telephone'):
            return TelephoneForm(request.POST)

    # if a GET (or any other method) it'll create a blank form
    else:
        if(part_of_profile_to_modify == 'description'):
            return DescriptionForm(old_description=data_person[part_of_profile_to_modify])
        if(part_of_profile_to_modify == 'telephone'):
            return TelephoneForm(old_telephone=data_person[part_of_profile_to_modify])


def person_profile_edition_display(request, part_of_profile_to_modify, ark_pid):
    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = Sparql_get_Person_methods().check_person_ark(ark_pid)
    
    if(sparql_request_check_person_ark):
        # Verify that the user is authenticated and has the right to modify the profile
        if (request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser)):

            data_person = Sparql_get_Person_methods().get_data_person(ark_pid)

            form = chose_form_to_display(request, part_of_profile_to_modify, data_person)
            # Check the request method
            if (request.method == 'POST'):
                if (form.is_valid()):
                    context = {
                        'message': "Vous pouvez éditer votre profil",
                        'data_person': data_person
                    }
                    Sparql_post_Person_methods().update_person_string_leaf(ark_pid, part_of_profile_to_modify, form.cleaned_data[part_of_profile_to_modify], data_person[part_of_profile_to_modify])
                    return redirect(person_edition_display, ark_pid=ark_pid)
            # return the form to be completed
            return render(request, 'person/edition/description_edition.html', {'form': form})

        else:
            # Check why the person cannot modify the profile and display the error
            if(request.user.is_authenticated):
                context = {
                    'message': "Vous n'avez pas le droit d'éditer ce profil"
                }
            else:
                context = {
                    'message': "Connectez-vous pour modifier votre profil"
                }
        
        return render(request, 'page_info.html', context)
    
    return render(request, 'page_404.html')