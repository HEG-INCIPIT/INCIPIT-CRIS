from django.db import models
from arketype_API.ark import Ark
from sparql_triplestore.sparql_requests.sparql_post_Person_methods import Sparql_post_Person_methods

class Person(models.Model):
    ark_pid = models.CharField(editable=False, max_length=100)
    given_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.ark_pid = Ark().ark_creation()
        sparql = Sparql_post_Person_methods()
        sparql.init_person(self.ark_pid, self.given_name, self.family_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}, {} {}'.format(self.ark_pid, self.given_name, self.family_name)
