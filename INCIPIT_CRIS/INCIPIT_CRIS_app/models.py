from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from arketype_API.ark import Ark
from sparql_triplestore.sparql_requests.sparql_post_Person_methods import Sparql_post_Person_methods

class User(AbstractUser):
    user = models.CharField(max_length=255)
    pass_w = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    ark_pid = models.CharField(blank=True, max_length=100)

    def save(self, *args, **kwargs):
        if(self.ark_pid == ''):
            self.ark_pid = Ark().ark_creation()
        sparql = Sparql_post_Person_methods()
        sparql.init_person(self.ark_pid, self.first_name, self.last_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ark_pid
