from django.shortcuts import render, HttpResponse
from django.template import loader
from sparql_triplestore.sparql_requests.sparql_get_Person_methods import Sparql_get_Person_methods

def persons_research(request):
    sparql_request = Sparql_get_Person_methods().get_persons()
    context = {
        'sparql_request': sparql_request
    }

    return render(request, 'display_results.html', context)

def person_display(request, ark_request):
    sparql_request_check_person_ark = Sparql_get_Person_methods().check_person_ark(ark_request)
    if(sparql_request_check_person_ark):
        data_person = Sparql_get_Person_methods().get_data_person(ark_request)
        return render(request, 'display_person_profile.html', data_person)
    
    return render(request, 'page_404.html')
