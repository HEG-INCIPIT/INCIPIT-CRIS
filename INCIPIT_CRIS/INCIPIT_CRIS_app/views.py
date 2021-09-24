from django.shortcuts import render
from .forms import *
from django.contrib.auth import get_user_model
from . import variables


def index(request):
    '''
    Search data of users from database, articles and project from triplestore and display it all
    in the template

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.

    Returns
    -------
    HttpResponse
        A HttpResponse object that is composed of a request object, the name of the template
        to display the index page and a dictionnary with all the data needed to fulfill
        the template.
    '''

    funders = variables.sparql_get_funder_object.get_funders()

    institutions = variables.sparql_get_institution_object.get_institutions()

    datasets = variables.sparql_get_dataset_object.get_datasets()

    articles = variables.sparql_get_article_object.get_articles()

    articles_data = []
    for article in articles:
        articles_data.append(variables.sparql_get_article_object.get_data_article(article[0]))
    articles_data.sort(key=lambda item: item['date_published'], reverse=True)

    user_model = get_user_model()
    users = user_model.objects.all().filter(is_staff=False).order_by('date_joined')

    last_users_registered = []
    for i in range(1, min(5+1, len(users)+1)):
        last_users_registered.append([users.values('pid')[len(users) - i]['pid'],
                                      users.values('first_name')[len(users) - i]['first_name'],
                                      users.values('last_name')[len(users) - i]['last_name']])

    projects = variables.sparql_get_project_object.get_projects()

    projects_data = []
    for project in projects:
        projects_data.append(variables.sparql_get_project_object.get_data_project(project[0]))
    projects_data.sort(key=lambda item: item['founding_date'], reverse=True)

    context = {
        'len_persons': len(users),
        'len_datasets': len(datasets),
        'len_institutions': len(institutions),
        'len_funders': len(funders),
        'len_articles': len(articles),
        'len_projects': len(projects_data),
        'last_users_registered': last_users_registered,
        'last_publications': articles_data[:5],
        'project_data': projects_data[:5],
    }
    return render(request, 'main/index.html', context)
