from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('personnes/', views.persons_research, name='person_research'),
    path('personnes/edition/profil/<str:part_of_profile_to_modify>/<path:ark_pid>', views.person_profile_edition_display, name='person_description_edition'),
    path('personnes/edition/<path:ark_pid>', views.person_edition_display, name='person_edition_display'),
    path('personnes/<path:ark_pid>', views.person_display, name='person_display'),

    path('articles/', views.articles_research, name='article_research'),
    path('articles/creation', views.articles_creation, name='articles_creation'),
]
