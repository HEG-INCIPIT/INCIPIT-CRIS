from django.shortcuts import render, HttpResponse
from django.urls import reverse
from sparql_triplestore.sparql_requests.sparql_get_Person_methods import Sparql_get_Person_methods

def index(request):
    return render(request, 'main/index.html')

def persons_research(request):
    sparql_request = Sparql_get_Person_methods().get_persons()
    context = {
        'sparql_request': sparql_request
    }

    return render(request, 'person/display_person_results.html', context)

def person_display(request, ark_pid):
    sparql_request_check_person_ark = Sparql_get_Person_methods().check_person_ark(ark_pid)
    if(sparql_request_check_person_ark):
        data_person = Sparql_get_Person_methods().get_data_person(ark_pid)
        context = {
            'data_person': data_person
        }
        return render(request, 'person/display_person_profile.html', context)
    
    return render(request, 'page_404.html')

def person_edition_display(request, ark_pid):
    sparql_request_check_person_ark = Sparql_get_Person_methods().check_person_ark(ark_pid)
    if(sparql_request_check_person_ark):
        if (request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser)):
            context = {
                'message': "Vous pouvez éditer votre profil"
            }
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