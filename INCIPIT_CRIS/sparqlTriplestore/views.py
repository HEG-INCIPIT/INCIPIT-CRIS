from django.shortcuts import render, HttpResponse

# Create your views here.

def pannel(request):
    return HttpResponse("Hello, world. You're at the polls index.")
