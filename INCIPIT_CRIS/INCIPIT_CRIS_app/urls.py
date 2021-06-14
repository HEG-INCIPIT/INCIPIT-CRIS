from django.urls import path

from . import views, views_person, views_article, views_project

urlpatterns = [
    path('', views.index, name='index'),

    path('personnes/', views_person.person_results, name='person_results'),
    path('personnes/edition/profil/deleteArticle/<path:ark_pid>', views_person.person_article_deletion, name='person_article_deletion'),
    path('personnes/edition/profil/<str:part_of_person_to_modify>/<path:ark_pid>', views_person.person_field_edition, name='person_field_edition'),
    path('personnes/edition/<path:ark_pid>', views_person.person_edition, name='person_edition_display'),
    path('personnes/<path:ark_pid>', views_person.person_profile, name='person_profile'),

    path('articles/', views_article.article_results, name='article_results'),
    path('articles/creation/', views_article.article_creation, name='article_creation'),
    path('articles/edition/field/addAuthor/<path:ark_pid>', views_article.article_author_addition, name='article_author_addition'),
    path('articles/edition/field/deleteAuthor/<path:ark_pid>', views_article.article_author_deletion, name='article_author_deletion'),
    path('articles/edition/field/deleteArticle/<path:ark_pid>', views_article.article_deletion, name='article_deletion'),
    path('articles/edition/field/<str:part_of_article_to_edit>/<path:ark_pid>', views_article.article_field_edition, name='article_field_edition'),
    path('articles/edition/<path:ark_pid>', views_article.article_edition, name='article_edition'),
    path('articles/<path:ark_pid>', views_article.article_profile, name='article_profile'),

    path('projects/', views_project.project_results, name='project_results'),
    path('projects/creation/', views_project.project_creation, name='project_creation'),
    path('projects/edition/field/deleteProject/<path:ark_pid>', views_project.project_deletion, name='project_deletion'),
    path('projects/edition/<path:ark_pid>', views_project.project_edition, name='project_edition'),
    path('projects/<path:ark_pid>', views_project.project_profile, name='project_profile'),
    
]
