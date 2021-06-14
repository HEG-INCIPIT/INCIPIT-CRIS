from django.shortcuts import render, redirect
from .forms import *
import re
import string
from . import views
from . import variables


def article_results(request):
    alphabet_list = list(string.ascii_lowercase)
    categories = ["Articles"]
    category = categories[0]
    sparql_request = variables.sparql_get_article_object.get_articles()
    context = {
        'sparql_request': sparql_request,
        'size_sparql_request': len(sparql_request),
        'alphabet_list': alphabet_list,
        'categories': categories,
        'category':category,
    }

    return render(request, 'article/article_results.html', context)


def article_profile(request, ark_pid):
    # Verify in triplestore if the ark_pid correspond to an article
    sparql_request_check_article_ark = variables.sparql_get_article_object.check_article_ark(ark_pid)
    if sparql_request_check_article_ark:
        data_article = variables.sparql_get_article_object.get_data_article(ark_pid)
        edition_granted = False
        if request.user.is_authenticated and request.user.ark_pid in [authors[0] for authors in data_article['authors']]:
            edition_granted = True
        context = {
            'edition_granted': edition_granted,
            'data_article': data_article
        }
        return render(request, 'article/article_profile.html', context)

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
                ark_pid = form.cleaned_data['ark_pid']
                if ark_pid == '':
                    ark_pid = variables.Ark().ark_creation()
                variables.sparql_post_article_object.create_article(ark_pid, form.cleaned_data['name'],
                                                          form.cleaned_data['abstract'],
                                                          form.cleaned_data['date_published'], form.cleaned_data['url'])
                for author in authors:
                    variables.sparql_post_article_object.add_author_to_article(ark_pid, author.split()[-1])
                return redirect(views.index)
        else:
            form = ArticleCreationForm()
        persons_info = variables.sparql_get_person_object.get_persons()
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
        authors_article = variables.sparql_get_article_object.get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser:
            edition_granted = True
            data_article = variables.sparql_get_article_object.get_data_article(ark_pid)
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


def article_form_selection(request, part_of_article_to_edit, data_article):
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
        authors_article = variables.sparql_get_article_object.get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser:

            data_article = variables.sparql_get_article_object.get_data_article(ark_pid)

            form = article_form_selection(request, part_of_article_to_edit, data_article)
            # Check the request method
            if request.method == 'POST':
                if form.is_valid():
                    if part_of_article_to_edit == 'datePublished':
                        variables.sparql_generic_post_object.update_date_leaf(ark_pid, part_of_article_to_edit,
                                                                    form.cleaned_data[part_of_article_to_edit],
                                                                    str(data_article[part_of_article_to_edit]) +
                                                                    " 00:00:00+00:00")
                    else:
                        variables.sparql_generic_post_object.update_string_leaf(ark_pid, part_of_article_to_edit,
                                                                      form.cleaned_data[part_of_article_to_edit],
                                                                      data_article[part_of_article_to_edit])
                    return redirect(article_edition, ark_pid=ark_pid)

            context = {
                'form': form,
                'button_value': 'Modifier',
                'url_to_return': '/articles/edition/field/{}/{}'.format(part_of_article_to_edit, ark_pid)
            }
            # return the form to be completed
            return render(request, 'forms/classic_form.html', context)

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
        authors_article = variables.sparql_get_article_object.get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser:

            data_article = variables.sparql_get_article_object.get_data_article(ark_pid)
            # Check the request method
            if request.method == 'POST':
                authors = re.findall('"([^"]*)"', request.POST['authorElementsPost'])
                for author in authors:
                    variables.sparql_post_article_object.add_author_to_article(ark_pid, author.split()[2])

                return redirect(article_edition, ark_pid=ark_pid)

            persons_info = variables.sparql_get_person_object.get_persons()
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
        authors_article = variables.sparql_get_article_object.get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser:
            author = request.POST.get('authorARK', '')
            variables.sparql_post_article_object.delete_author_of_article(ark_pid, author)

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
        authors_article = variables.sparql_get_article_object.get_authors_article(ark_pid)
        # Verify if the user ark is in the articles authors to grant edition
        if request.user.ark_pid in [authors[0] for authors in authors_article] or request.user.is_superuser:
            variables.sparql_post_article_object.delete_article(ark_pid)

            return redirect(views.index)

        context = {
            'message': "Vous n'avez pas le droit d'éditer cet article",
        }
        return render(request, 'page_info.html', context)
    context = {
        'message': "Connectez-vous pour pouvoir éditer cet article"
    }
    return render(request, 'page_info.html', context)
