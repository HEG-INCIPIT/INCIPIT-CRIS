from django.forms.forms import Form
from .models import *
from django.shortcuts import render, redirect
from .forms import *
import re
from django.contrib.auth import get_user_model
import string
from arketype_API.ark import Ark
from sparql_triplestore.sparql_requests.sparql_generic_post_methods import SparqlGenericPostMethods
from sparql_triplestore.sparql_requests.person.sparql_get_Person_methods import SparqlGetPersonMethods
from sparql_triplestore.sparql_requests.person.sparql_post_Person_methods import SparqlPostPersonMethods
from sparql_triplestore.sparql_requests.articles.sparql_get_articles_methods import SparqlGetArticlesMethods
from sparql_triplestore.sparql_requests.articles.sparql_post_articles_methods import SparqlPostArticlesMethods
from sparql_triplestore.sparql_requests.projects.sparql_get_projects_methods import SparqlGetProjectsMethods
from sparql_triplestore.sparql_requests.projects.sparql_post_projects_methods import SparqlPostProjectsMethods

sparql_generic_post_object = SparqlGenericPostMethods()
sparql_get_person_object = SparqlGetPersonMethods()
sparql_get_article_object = SparqlGetArticlesMethods()
sparql_post_article_object = SparqlPostArticlesMethods()
sparql_get_project_object = SparqlGetProjectsMethods()
sparql_post_project_object = SparqlPostProjectsMethods()


def index(request):
    """
    Compute data of users from database, articles and project from triplestore for the template
    :param request: object
    :return: render function with template and data
    """
    articles = sparql_get_article_object.get_articles()

    articles_data = []
    for article in articles:
        articles_data.append(sparql_get_article_object.get_data_article(article[0]))
    articles_data.sort(key=lambda item: item['datePublished'], reverse=True)

    user_model = get_user_model()
    users = user_model.objects.all().filter(is_staff=False).order_by('date_joined')

    last_users_registered = []
    for i in range(1, 6):
        last_users_registered.append([users.values('ark_pid')[len(users) - i]['ark_pid'],
                                      users.values('first_name')[len(users) - i]['first_name'],
                                      users.values('last_name')[len(users) - i]['last_name']])

    projects = sparql_get_project_object.get_projects()

    projects_data = []
    for project in projects:
        projects_data.append(sparql_get_project_object.get_data_project(project[0]))
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


##################################################
# Person
##################################################


def persons_research(request):
    """
    Compute a research of all persons in triplestore for the template
    :param request:
    :return: render function with template and data
    """
    alphabet_list = list(string.ascii_lowercase)
    categories = ["Personnes", "Professeurs ordinaire", "Assistants HES"]
    category = categories[0]
    sparql_request = sparql_get_person_object.get_persons()
    context = {
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
    }

    return render(request, 'person/display_person_results.html', context)


def person_display(request, ark_pid):
    """
    Display a page with all the data of the person given by the ark_pid
    :param request: object
    :param ark_pid: string -> Person identifier
    :return: render function with template and data
    """
    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = sparql_get_person_object.check_person_ark(ark_pid)
    can_edit = True if request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser) else False
    if sparql_request_check_person_ark:
        data_person = sparql_get_person_object.get_data_person(ark_pid)
        context = {
            'data_person': data_person,
            'can_edit': can_edit,
            'ark_pid': ark_pid,
        }
        return render(request, 'person/display_person_profile.html', context)

    return render(request, 'page_404.html')


def person_edition_display(request, ark_pid):
    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = sparql_get_person_object.check_person_ark(ark_pid)
    if sparql_request_check_person_ark:
        if request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser):
            data_person = sparql_get_person_object.get_data_person(ark_pid)
            context = {
                'data_person': data_person,
                'ark_pid': ark_pid
            }
            return render(request, 'person/display_person_for_edition.html', context)
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


def person_chose_form_to_display(request, part_of_profile_to_modify, data_person):
    # Check the request method
    if request.method == 'POST':
        if part_of_profile_to_modify == 'description':
            return DescriptionForm(request.POST)
        if part_of_profile_to_modify == 'telephone':
            return TelephoneForm(request.POST)

    # if not a POST it'll create a blank form
    else:
        if part_of_profile_to_modify == 'description':
            return DescriptionForm(old_description=data_person[part_of_profile_to_modify])
        if part_of_profile_to_modify == 'telephone':
            return TelephoneForm(old_telephone=data_person[part_of_profile_to_modify])


def person_profile_edition_display(request, part_of_profile_to_modify, ark_pid):
    context = {}
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_person_ark = sparql_get_person_object.check_person_ark(ark_pid)

    if sparql_request_check_person_ark:
        # Verify that the user is authenticated and has the right to modify the profile
        if request.user.is_authenticated and (request.user.ark_pid == ark_pid or request.user.is_superuser):

            data_person = sparql_get_person_object.get_data_person(ark_pid)

            form = person_chose_form_to_display(request, part_of_profile_to_modify, data_person)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    sparql_generic_post_object.update_string_leaf(ark_pid, part_of_profile_to_modify,
                                                                  form.cleaned_data[part_of_profile_to_modify],
                                                                  data_person[part_of_profile_to_modify])
                    return redirect(person_edition_display, ark_pid=ark_pid)

            context = {
                'form': form,
                'button_value': 'Modifier',
                'url_to_return': '/personnes/edition/profil/{}/{}'.format(part_of_profile_to_modify, ark_pid)
            }
            # return the form to be completed
            return render(request, 'forms/person/person_profil_edition.html', context)

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
            sparql_post_article_object.delete_author_of_article(article, ark_pid)

            return redirect(person_edition_display, ark_pid=ark_pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


##################################################
# Articles
##################################################

def article_research(request):
    alphabet_list = list(string.ascii_lowercase)
    categories = ["Articles"]
    category = categories[0]
    sparql_request = sparql_get_article_object.get_articles()
    context = {
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
    }

    return render(request, 'article/display_articles_results.html', context)


def article_display(request, ark_pid):
    # Verify in triplestore if the ark_pid correspond to an article
    sparql_request_check_article_ark = sparql_get_article_object.check_article_ark(ark_pid)
    if sparql_request_check_article_ark:
        data_article = sparql_get_article_object.get_data_article(ark_pid)
        edition_granted = False
        if request.user.is_authenticated and request.user.ark_pid in [authors[0] for authors in data_article['authors']]:
            edition_granted = True
        context = {
            'edition_granted': edition_granted,
            'data_article': data_article
        }
        return render(request, 'article/display_article_profile.html', context)

    return render(request, 'page_404.html')


def article_creation(request):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Check the request method
        if request.method == 'POST':
            form = ArticleCreationForm(request.POST)
            if form.is_valid():
                authors = re.findall('"([^"]*)"', request.POST['authorElementsPost'])
                print(authors)
                ark_pid = form.cleaned_data['ark_pid']
                if ark_pid == '':
                    ark_pid = Ark().ark_creation()
                sparql_post_article_object.create_article(ark_pid, form.cleaned_data['name'],
                                                          form.cleaned_data['abstract'],
                                                          form.cleaned_data['date_published'], form.cleaned_data['url'])
                for author in authors:
                    sparql_post_article_object.add_author_to_article(ark_pid, author.split()[-1])
                return redirect(index)
        else:
            form = ArticleCreationForm()
        persons_info = sparql_get_person_object.get_persons()
        persons = []
        for basic_info_person in persons_info:
            persons.append('''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))
        context = {
            'form': form,
            'button_value': 'Créer',
            'url_to_return': '/articles/creation/',
            'persons': persons
        }
        # return the form to be completed
        return render(request, 'forms/article/article_creation.html', context)

    else:
        context = {
            'message': "Connectez-vous pour pourvoir créer des articles"
        }

        return render(request, 'page_info.html', context)


def article_edition(request, ark_pid):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = sparql_get_article_object.get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser:
            edition_granted = True
            data_article = sparql_get_article_object.get_data_article(ark_pid)
            context = {
                'edition_granted': edition_granted,
                'data_article': data_article
            }
            return render(request, 'article/article_profile_edition.html', context)

        edition_granted = False
        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
            'edition_granted': edition_granted
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_chose_form_to_display(request, part_of_article_to_edit, data_article):
    # Check the request method
    if request.method == 'POST':
        if part_of_article_to_edit == 'name':
            return ArticleNameForm(request.POST)
        if part_of_article_to_edit == 'abstract':
            return ArticleAbstractForm(request.POST)
        if part_of_article_to_edit == 'datePublished':
            return ArticleDatePublishedForm(request.POST)

    # if not a POST it'll create a blank form
    else:
        if part_of_article_to_edit == 'name':
            return ArticleNameForm(old_name=data_article[part_of_article_to_edit])
        if part_of_article_to_edit == 'abstract':
            return ArticleAbstractForm(old_abstract=data_article[part_of_article_to_edit])
        if part_of_article_to_edit == 'datePublished':
            return ArticleDatePublishedForm(old_date_published=data_article[part_of_article_to_edit])


def article_field_edition(request, part_of_article_to_edit, ark_pid):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = sparql_get_article_object.get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser:

            data_article = sparql_get_article_object.get_data_article(ark_pid)

            form = article_chose_form_to_display(request, part_of_article_to_edit, data_article)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    if part_of_article_to_edit == 'datePublished':
                        sparql_generic_post_object.update_date_leaf(ark_pid, part_of_article_to_edit,
                                                                    form.cleaned_data[part_of_article_to_edit],
                                                                    str(data_article[part_of_article_to_edit]) +
                                                                    " 00:00:00+00:00")
                    else:
                        sparql_generic_post_object.update_string_leaf(ark_pid, part_of_article_to_edit,
                                                                      form.cleaned_data[part_of_article_to_edit],
                                                                      data_article[part_of_article_to_edit])
                    return redirect(article_edition, ark_pid=ark_pid)

            context = {
                'form': form,
                'button_value': 'Modifier',
                'url_to_return': '/articles/edition/field/{}/{}'.format(part_of_article_to_edit, ark_pid)
            }
            # return the form to be completed
            return render(request, 'forms/classic_form_display.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_author_addition(request, ark_pid):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = sparql_get_article_object.get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser:

            data_article = sparql_get_article_object.get_data_article(ark_pid)
            # Check the request method
            if request.method == 'POST':
                authors = re.findall('"([^"]*)"', request.POST['authorElementsPost'])
                for author in authors:
                    sparql_post_article_object.add_author_to_article(ark_pid, author.split()[2])

                return redirect(article_edition, ark_pid=ark_pid)

            persons_info = sparql_get_person_object.get_persons()
            persons = []
            for basic_info_person in persons_info:
                if not (basic_info_person[0] in [author[0] for author in authors_article]):
                    persons.append(
                        '''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))

            context = {
                'button_value': 'Ajouter',
                'url_to_return': '/articles/edition/field/addAuthor/{}'.format(ark_pid),
                'persons': persons
            }
            # return the form to be completed
            return render(request, 'forms/article/article_add_author.html', context)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_author_deletion(request, ark_pid):
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = sparql_get_article_object.get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser:
            author = request.POST.get('authorARK', '')
            sparql_post_article_object.delete_author_of_article(ark_pid, author)

            return redirect(article_edition, ark_pid=ark_pid)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)


def article_deletion(request, ark_pid):
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the authors of the article
        authors_article = sparql_get_article_object.get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser:
            sparql_post_article_object.delete_article(ark_pid)

            return redirect(index)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)

##################################################
# Projects
##################################################

def projetcts_research(request):
    alphabet_list = list(string.ascii_lowercase)
    categories = ["Projets de recherche"]
    category = categories[0]
    sparql_request = sparql_get_project_object.get_projects()
    context = {
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
    }

    return render(request, 'project/display_projects_results.html', context)


def project_creation(request):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Check the request method
        if request.method == 'POST':
            form = ProjectCreationForm(request.POST)
            if form.is_valid():
                members = re.findall('"([^"]*)"', request.POST['memberElementsPost'])
                print(members)
                ark_pid = form.cleaned_data['ark_pid']
                if ark_pid == '':
                    ark_pid = Ark().ark_creation()
                sparql_post_project_object.create_project(ark_pid, form.cleaned_data['name'],
                                                          form.cleaned_data['description'],
                                                          form.cleaned_data['founding_date'], form.cleaned_data['url'])
                for member in members:
                    sparql_post_project_object.add_member_to_project(ark_pid, member.split()[-1])
                return redirect(index)
        else:
            form = ProjectCreationForm()
        persons_info = sparql_get_person_object.get_persons()
        persons = []
        for basic_info_person in persons_info:
            persons.append('''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))
        context = {
            'form': form,
            'button_value': 'Créer',
            'url_to_return': '/projects/creation/',
            'persons': persons
        }
        # return the form to be completed
        return render(request, 'forms/project/project_creation.html', context)

    else:
        context = {
            'message': "Connectez-vous pour pourvoir créer des projets"
        }

        return render(request, 'page_info.html', context)


def project_display(request, ark_pid):
    # Verify in triplestore if the ark_pid correspond to a project
    sparql_request_check_project_ark = sparql_get_project_object.check_project_ark(ark_pid)
    print(ark_pid)
    if sparql_request_check_project_ark:
        data_project = sparql_get_project_object.get_data_project(ark_pid)
        edition_granted = False
        if request.user.is_authenticated and request.user.ark_pid in [members[0] for members in data_project['members']]:
            edition_granted = True
        context = {
            'edition_granted': edition_granted,
            'data_project': data_project
        }
        return render(request, 'project/display_project_profile.html', context)

    return render(request, 'page_404.html')

def project_edition(request, ark_pid):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:
            edition_granted = True
            data_project = sparql_get_project_object.get_data_project(ark_pid)
            context = {
                'edition_granted': edition_granted,
                'data_project': data_project
            }
            return render(request, 'project/project_profile_edition.html', context)

        edition_granted = False
        context = {
            'message': "Vous n'avez pas le droit d'éditer cet project",
            'edition_granted': edition_granted
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet project"
    }
    return render(request, 'page_info.html', context)





def project_deletion(request, ark_pid):
    # Verify that the user is authenticated and has the right to modify the profile
    if request.user.is_authenticated:
        # Request all the members of the project
        members_project = sparql_get_project_object.get_members_project(ark_pid)
        # Verify if the user ark is in the projects members to grant edition
        if request.user.ark_pid in [members[0] for members in members_project] or request.user.is_superuser:
            sparql_post_project_object.delete_project(ark_pid)

            return redirect(index)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet projet",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet projet"
    }
    return render(request, 'page_info.html', context)