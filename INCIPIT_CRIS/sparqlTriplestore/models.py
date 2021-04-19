from django.db import models
from .sparqlPostMethods import Sparql_post_methods

class Person(models.Model):
    ark = models.Field(editable = False)
    given_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.ark = 'ark00000001'
        sparql = Sparql_post_methods()
        sparql.init_person(self.ark, self.given_name, self.family_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}, {} {}'.format(self.ark, self.given_name, self.family_name)
