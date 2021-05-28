from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from arketype_API.ark import Ark
from sparql_triplestore.sparql_requests.person.sparql_post_Person_methods import Sparql_post_Person_methods
from sparql_triplestore.sparql_requests.person.sparql_get_Person_methods import Sparql_get_Person_methods


class User(AbstractUser):
    user = models.CharField(max_length=255)
    pass_w = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    ark_pid = models.CharField(blank=True, max_length=100)

    # var to verify at each save of a user if those elements changed
    __original_email = None
    __original_first_name = None
    __original_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_email = self.email
        self.__original_first_name = self.first_name
        self.__original_last_name = self.last_name

    def save(self, *args, **kwargs):
        if (not Sparql_get_Person_methods().check_person_ark(self.ark_pid) and not self.is_staff):
            if (self.ark_pid == ''):
                self.ark_pid = Ark().ark_creation()
            sparql = Sparql_post_Person_methods()
            sparql.init_person(self.ark_pid, self.first_name, self.last_name, self.email)
        if (self.email != self.__original_email):
            Sparql_post_Person_methods().update_person_string_leaf(self.ark_pid, 'email', self.email,
                                                                   self.__original_email)
        if (self.first_name != self.__original_first_name):
            Sparql_post_Person_methods().update_person_string_leaf(self.ark_pid, 'givenName', self.first_name,
                                                                   self.__original_first_name)
        if (self.last_name != self.__original_last_name):
            Sparql_post_Person_methods().update_person_string_leaf(self.ark_pid, 'familyName', self.last_name,
                                                                   self.__original_last_name)

        super().save(*args, **kwargs)
        self.__original_email = self.email
        self.__original_first_name = self.first_name
        self.__original_last_name = self.last_name

    def __str__(self):
        return self.ark_pid
