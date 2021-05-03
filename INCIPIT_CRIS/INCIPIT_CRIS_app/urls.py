from django.urls import path

from . import views

urlpatterns = [
    path('personnes/', views.persons_research),
    path('personnes/<path:ark_request>', views.person_display, name='person_display'),
    path('', views.index, name='index'),
]
