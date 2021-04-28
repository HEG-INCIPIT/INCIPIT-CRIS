from django.urls import path

from . import views

urlpatterns = [
    path('', views.persons_research),
    path('<path:ark_request>', views.person_display, name='person_display'),
]
