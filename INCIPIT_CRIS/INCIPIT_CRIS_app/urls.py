from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('personnes/', views.persons_research, name='person_research'),
    path('personnes/edition/profil/deleteArticle/<path:ark_pid>', views.person_article_deletion, name='person_article_deletion'),
    path('personnes/edition/profil/<str:part_of_profile_to_modify>/<path:ark_pid>', views.person_profile_edition_display, name='person_description_edition'),
    path('personnes/edition/<path:ark_pid>', views.person_edition_display, name='person_edition_display'),
    path('personnes/<path:ark_pid>', views.person_display, name='person_display'),

    path('articles/', views.article_research, name='article_research'),
    path('articles/creation/', views.article_creation, name='article_creation'),
    path('articles/edition/field/addAuthor/<path:ark_pid>', views.article_author_addition, name='article_author_addition'),
    path('articles/edition/field/deleteAuthor/<path:ark_pid>', views.article_author_deletion, name='article_author_deletion'),
    path('articles/edition/field/deleteArticle/<path:ark_pid>', views.article_deletion, name='article_deletion'),
    path('articles/edition/field/<str:part_of_article_to_edit>/<path:ark_pid>', views.article_field_edition, name='article_field_edition'),
    path('articles/edition/<path:ark_pid>', views.article_edition, name='article_edition'),
    path('articles/<path:ark_pid>', views.article_display, name='article_display'),

    path('projects/', views.projetcts_research, name='projetcts_research'),
    path('projects/creation/', views.project_creation, name='project_creation'),
    path('projects/edition/field/deleteProject/<path:ark_pid>', views.project_deletion, name='project_deletion'),
    path('projects/edition/<path:ark_pid>', views.project_edition, name='project_edition'),
    path('projects/<path:ark_pid>', views.project_display, name='project_display'),
    
]
