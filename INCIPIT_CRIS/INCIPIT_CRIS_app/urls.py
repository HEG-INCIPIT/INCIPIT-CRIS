from django.urls import path

from . import views, views_person, views_article, views_project, views_dataset

urlpatterns = [
    path('', views.index, name='index'),

    path('personnes/', views_person.person_results, name='person_results'),
    path('personnes/edition/profil/add-article/<path:ark_pid>', views_person.person_article_addition, name='person_article_addition'),
    path('personnes/edition/profil/delete-article/<path:ark_pid>', views_person.person_article_deletion, name='person_article_deletion'),
    path('personnes/edition/profil/add-project/<path:ark_pid>', views_person.person_project_addition, name='person_project_addition'),
    path('personnes/edition/profil/delete-project/<path:ark_pid>', views_person.person_project_deletion, name='person_project_deletion'),
    path('personnes/edition/profil/<str:part_of_person_to_modify>/<path:ark_pid>', views_person.person_field_edition, name='person_field_edition'),
    path('personnes/edition/<path:ark_pid>', views_person.person_edition, name='person_edition_display'),
    path('personnes/<path:ark_pid>', views_person.person_profile, name='person_profile'),

    path('articles/', views_article.article_results, name='article_results'),
    path('articles/creation/', views_article.article_creation, name='article_creation'),
    path('articles/edition/field/add-author/<path:ark_pid>', views_article.article_author_addition, name='article_author_addition'),
    path('articles/edition/field/delete-author/<path:ark_pid>', views_article.article_author_deletion, name='article_author_deletion'),
    path('articles/edition/field/add-project/<path:ark_pid>', views_article.article_project_addition, name='article_project_addition'),
    path('articles/edition/field/delete-project/<path:ark_pid>', views_article.article_project_deletion, name='article_project_deletion'),
    path('articles/edition/delete-article/<path:ark_pid>', views_article.article_deletion, name='article_deletion'),
    path('articles/edition/field/<str:part_of_article_to_edit>/<path:ark_pid>', views_article.article_field_edition, name='article_field_edition'),
    path('articles/edition/<path:ark_pid>', views_article.article_edition, name='article_edition'),
    path('articles/<path:ark_pid>', views_article.article_profile, name='article_profile'),

    path('projects/', views_project.project_results, name='project_results'),
    path('projects/creation/', views_project.project_creation, name='project_creation'),
    path('projects/edition/field/add-member/<path:ark_pid>', views_project.project_member_addition, name='project_member_addition'),
    path('projects/edition/field/delete-member/<path:ark_pid>', views_project.project_member_deletion, name='project_member_deletion'),
    path('projects/edition/delete-project/<path:ark_pid>', views_project.project_deletion, name='project_deletion'),
    path('projects/edition/field/add-article/<path:ark_pid>', views_project.project_article_addition, name='project_article_addition'),
    path('projects/edition/field/delete-article/<path:ark_pid>', views_project.project_article_deletion, name='project_article_deletion'),
    path('projects/edition/field/<str:part_of_project_to_edit>/<path:ark_pid>', views_project.project_field_edition, name='project_field_edition'),
    path('projects/edition/<path:ark_pid>', views_project.project_edition, name='project_edition'),
    path('projects/<path:ark_pid>', views_project.project_profile, name='project_profile'),

    path('datasets/', views_dataset.dataset_results, name='dataset_results'),
    path('datasets/creation/', views_dataset.dataset_creation, name='dataset_creation'),
    path('datasets/edition/delete-dataset/<path:ark_pid>', views_dataset.dataset_deletion, name='dataset_deletion'),
    path('datasets/edition/field/<str:part_of_dataset_to_edit>/<path:ark_pid>', views_dataset.dataset_field_edition, name='dataset_field_edition'),
    path('datasets/edition/<path:ark_pid>', views_dataset.dataset_edition, name='dataset_edition'),
    path('datasets/<path:ark_pid>', views_dataset.dataset_profile, name='dataset_profile'),
    
]
