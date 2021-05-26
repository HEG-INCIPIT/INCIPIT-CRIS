from django.forms.forms import Form
from .models import *
from django.shortcuts import render, redirect
from .forms import *
import re
from arketype_API.ark import Ark
from sparql_triplestore.sparql_requests.sparql_generic_post_methods import Sparql_generic_post_methods
from sparql_triplestore.sparql_requests.person.sparql_get_Person_methods import Sparql_get_Person_methods
from sparql_triplestore.sparql_requests.person.sparql_post_Person_methods import Sparql_post_Person_methods
from sparql_triplestore.sparql_requests.articles.sparql_get_articles_methods import Sparql_get_articles_methods
from sparql_triplestore.sparql_requests.articles.sparql_post_articles_methods import Sparql_post_articles_methods

def index(request):
    persons = len(Sparql_get_Person_methods().get_persons())
    articles = len(Sparql_get_articles_methods().get_articles())
    context = {
        'persons': persons,
        'articles': articles,
    }
    return render(request, 'main/index.html')

##################################################
# Person
##################################################

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
                'data_person': data_person,
                'ark_pid': ark_pid
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


def person_chose_form_to_display(request, part_of_profile_to_modify, data_person):
    # Check the request method
    if (request.method == 'POST'):
        if(part_of_profile_to_modify == 'description'):
            return DescriptionForm(request.POST)
        if(part_of_profile_to_modify == 'telephone'):
            return TelephoneForm(request.POST)

    # if not a POST it'll create a blank form
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

            form = person_chose_form_to_display(request, part_of_profile_to_modify, data_person)
            # Check the request method
            if (request.method == 'POST'):
                if (form.is_valid()):
                    
                    Sparql_generic_post_methods().update_string_leaf(ark_pid, part_of_profile_to_modify, form.cleaned_data[part_of_profile_to_modify], data_person[part_of_profile_to_modify])
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

def person_article_deletion(request, ark_pid):
    # Verify that the user is authenticated and has the right to modify the profile
    if (request.user.is_authenticated):
        # Verify that the edition of profile is made by the legitimate user or admin
        if(request.user.ark_pid == ark_pid or request.user.is_superuser):
            
            article = request.POST.get('articleARK', '')
            Sparql_post_articles_methods().delete_author_of_article(article, ark_pid)

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
    sparql_request = Sparql_get_articles_methods().get_articles()
    context = {
        'sparql_request': sparql_request
    }

    return render(request, 'article/display_articles_results.html', context)

def article_display(request, ark_pid):
    # Verify in triplestore if the ark_pid correspond to a person
    sparql_request_check_article_ark = Sparql_get_articles_methods().check_article_ark(ark_pid)
    if(sparql_request_check_article_ark):
        data_article = Sparql_get_articles_methods().get_data_article(ark_pid)
        edition_granted = False
        if(request.user.ark_pid in [authors[0] for authors in data_article['authors']]):
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
    if (request.user.is_authenticated):
        # Check the request method
        if (request.method == 'POST'):
            form = ArticleCreationForm(request.POST)
            if (form.is_valid()):
                authors = re.findall('"([^"]*)"', request.POST['authorElementsPost'])
                ark_pid = form.cleaned_data['ark_pid']
                if(ark_pid == ''):
                    ark_pid = Ark().ark_creation()
                Sparql_post_articles_methods().create_article(ark_pid, form.cleaned_data['name'], form.cleaned_data['abstract'], form.cleaned_data['date_published'])
                for author in authors:
                    Sparql_post_articles_methods().add_author_to_article(ark_pid, author.split()[2])
                return redirect(index)
        else:
            form = ArticleCreationForm()
        persons_info = Sparql_get_Person_methods().get_persons()
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
    if (request.user.is_authenticated):
        # Request all the authors of the article
        authors_article = Sparql_get_articles_methods().get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if(request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser):
            edition_granted = True
            data_article = Sparql_get_articles_methods().get_data_article(ark_pid)
            context = {
                    'message': "Vous pouvez éditer cet article",
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
    if (request.method == 'POST'):
        if(part_of_article_to_edit == 'name'):
            return ArticleNameForm(request.POST)
        if(part_of_article_to_edit == 'abstract'):
            return ArticleAbstractForm(request.POST)
        if(part_of_article_to_edit == 'datePublished'):
            return ArticleDatePublishedForm(request.POST)

    # if not a POST it'll create a blank form
    else:
        if(part_of_article_to_edit == 'name'):
            return ArticleNameForm(old_name=data_article[part_of_article_to_edit])
        if(part_of_article_to_edit == 'abstract'):
            return ArticleAbstractForm(old_abstract=data_article[part_of_article_to_edit])
        if(part_of_article_to_edit == 'datePublished'):
            return ArticleDatePublishedForm(old_datePublished=data_article[part_of_article_to_edit])

def article_field_edition(request, part_of_article_to_edit, ark_pid):
    context = {}
    # Verify that the user is authenticated and has the right to modify the profile
    if (request.user.is_authenticated):
        # Request all the authors of the article
        authors_article = Sparql_get_articles_methods().get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if(request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser):
            
            data_article = Sparql_get_articles_methods().get_data_article(ark_pid)

            form = article_chose_form_to_display(request, part_of_article_to_edit, data_article)
            # Check the request method
            if (request.method == 'POST'):
                if (form.is_valid()):
                    if(part_of_article_to_edit == 'datePublished'):
                        Sparql_generic_post_methods().update_date_leaf(ark_pid, part_of_article_to_edit, form.cleaned_data[part_of_article_to_edit], str(data_article[part_of_article_to_edit])+" 00:00:00+00:00")
                    else:
                        Sparql_generic_post_methods().update_string_leaf(ark_pid, part_of_article_to_edit, form.cleaned_data[part_of_article_to_edit], data_article[part_of_article_to_edit])
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
    if (request.user.is_authenticated):
        # Request all the authors of the article
        authors_article = Sparql_get_articles_methods().get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if(request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser):
            
            data_article = Sparql_get_articles_methods().get_data_article(ark_pid)
            # Check the request method
            if (request.method == 'POST'):
                authors = re.findall('"([^"]*)"', request.POST['authorElementsPost'])
                for author in authors:
                    Sparql_post_articles_methods().add_author_to_article(ark_pid, author.split()[2])

                return redirect(article_edition, ark_pid=ark_pid)

            persons_info = Sparql_get_Person_methods().get_persons()
            persons = []
            for basic_info_person in persons_info:
                if(not (basic_info_person[0] in [author[0] for author in authors_article])):
                    persons.append('''{} {}, {}'''.format(basic_info_person[1], basic_info_person[2], basic_info_person[0]))

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
    if (request.user.is_authenticated):
        # Request all the authors of the article
        authors_article = Sparql_get_articles_methods().get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if(request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser):
            
            author = request.POST.get('authorARK', '')
            Sparql_post_articles_methods().delete_author_of_article(ark_pid, author)

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
    if (request.user.is_authenticated):
        # Request all the authors of the article
        authors_article = Sparql_get_articles_methods().get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if(request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser):
            
            Sparql_post_articles_methods().delete_article(ark_pid)

            return redirect(index)
        
        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)