from django.shortcuts import render
from .forms import *
from django.contrib.auth import get_user_model
from . import variables


def index(request):
    """
    Compute data of users from database, articles and project from triplestore for the template
    :param request: object
    :return: render function with template and data
    """
    articles = variables.sparql_get_article_object.get_articles()

    articles_data = []
    for article in articles:
        articles_data.append(variables.sparql_get_article_object.get_data_article(article[0]))
    articles_data.sort(key=lambda item: item['date_published'], reverse=True)

    user_model = get_user_model()
    users = user_model.objects.all().filter(is_staff=False).order_by('date_joined')

    last_users_registered = []
    for i in range(1, 6):
        last_users_registered.append([users.values('ark_pid')[len(users) - i]['ark_pid'],
                                      users.values('first_name')[len(users) - i]['first_name'],
                                      users.values('last_name')[len(users) - i]['last_name']])

    projects = variables.sparql_get_project_object.get_projects()

    projects_data = []
    for project in projects:
        projects_data.append(variables.sparql_get_project_object.get_data_project(project[0]))
    projects_data.sort(key=lambda item: item['founding_date'], reverse=True)

    context = {
        'len_persons': len(users),
        'len_articles': len(articles),
        'len_projects': len(projects_data),
        'last_users_registered': last_users_registered,
        'last_publications': articles_data[:5],
        'project_data': projects_data[:5],
    }
    return render(request, 'main/index.html', context)
