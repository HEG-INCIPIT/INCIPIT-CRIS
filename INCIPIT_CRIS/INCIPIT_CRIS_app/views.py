from django.shortcuts import render, HttpResponse
from sparql_triplestore.sparql_requests.sparql_get_Person_methods import Sparql_get_Person_methods

def persons_research(request):
    sparql_request = Sparql_get_Person_methods().get_persons()
    return HttpResponse(sparql_request)

def person_display(request, ark_request):
    sparql_request = Sparql_get_Person_methods().check_person_ark(ark_request)
    return HttpResponse(sparql_request)
