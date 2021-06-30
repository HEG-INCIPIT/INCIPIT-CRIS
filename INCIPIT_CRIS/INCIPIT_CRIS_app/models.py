from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from . import variables


class User(AbstractUser):
    user = models.CharField(max_length=255)
    pass_w = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    ark_pid = models.CharField(blank=True, max_length=100)

    # variables to verify at each save of a user if those elements changed
    __original_email = None
    __original_first_name = None
    __original_last_name = None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_email = self.email
        self.__original_first_name = self.first_name
        self.__original_last_name = self.last_name


    def save(self, *args, **kwargs):
        if not variables.sparql_get_person_object.check_person_ark(self.ark_pid) and not self.is_staff:
            if self.ark_pid == '':
                self.ark_pid = variables.ark.ark_creation()
            variables.sparql_post_person_object.init_person(self.ark_pid, self.first_name, self.last_name, self.email)
            if self.email != self.__original_email:
                variables.sparql_post_person_object.update_person_string_leaf(self.ark_pid, 'email', self.email,
                                                                        self.__original_email)
            if self.first_name != self.__original_first_name:
                variables.sparql_post_person_object.update_person_string_leaf(self.ark_pid, 'givenName', self.first_name,
                                                                        self.__original_first_name)
            if self.last_name != self.__original_last_name:
                variables.sparql_post_person_object.update_person_string_leaf(self.ark_pid, 'familyName', self.last_name,
                                                                        self.__original_last_name)

        super().save(*args, **kwargs)
        self.__original_email = self.email
        self.__original_first_name = self.first_name
        self.__original_last_name = self.last_name


    def __str__(self):
        return self.ark_pid

@receiver(pre_delete, sender=User)
def delete_in_sparql(sender, instance, using, **kwargs):
    variables.sparql_generic_post_object.delete_subject(str(instance))
    variables.sparql_generic_post_object.delete_subject(str(instance)+"ARK")