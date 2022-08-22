from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from . import variables
from django.conf import settings
import datetime


class User(AbstractUser):
    user = models.CharField(max_length=255)
    pass_w = models.CharField(max_length=50)
    email = models.EmailField('Adresse mail', unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    pid = models.CharField(blank=True, max_length=100)

    # Photo
    #photo = models.ImageField(upload_to='profile_photos/')

    # ORCID
    access_token_orcid = models.CharField(max_length=100, blank=True)
    refresh_token_orcid = models.CharField(max_length=100, blank=True)
    expires_in_orcid = models.CharField(max_length=100, blank=True)
    orcid = models.CharField(max_length=30, blank=True)

    # variables to verify at each save of a user if those elements changed
    __original_email = ''
    __original_first_name = ''
    __original_last_name = ''
    __original_orcid = ''


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_email = self.email
        self.__original_first_name = self.first_name
        self.__original_last_name = self.last_name
        self.__original_orcid = self.orcid


    def save(self, *args, **kwargs):
        if  not self.is_staff and not variables.sparql_get_person_object.check_person_ark(self.pid):
            if self.pid == '':
                
                try:
                    self.pid = variables.ark.mint('', '{} {}'.format(self.first_name, self.last_name), 
                        'An ARK created in INCIPIT-CRIS for a person named {} {}'.format(self.first_name, self.last_name), datetime.datetime.now())
                    variables.ark.update('{}'.format(self.pid), '{}{}'.format(settings.URL, self.pid), '{} {}'.format(self.first_name, self.last_name), 
                        'An ARK created in INCIPIT-CRIS for a person named {} {}'.format(self.first_name, self.last_name), datetime.datetime.now())
                except:
                    print("ERROR")
                    raise Exception

            variables.sparql_post_person_object.init_person(self.pid, self.first_name, self.last_name, self.email)
        if self.email != self.__original_email:
            variables.sparql_post_person_object.update_person_string_leaf(self.pid, 'email', self.email,
                                                                    self.__original_email)
        if self.first_name != self.__original_first_name:
            variables.sparql_post_person_object.update_person_string_leaf(self.pid, 'givenName', self.first_name,
                                                                    self.__original_first_name)
        if self.last_name != self.__original_last_name:
            variables.sparql_post_person_object.update_person_string_leaf(self.pid, 'familyName', self.last_name,
                                                                    self.__original_last_name)
        if self.orcid != self.__original_orcid:
            variables.sparql_post_person_object.update_person_string_leaf(self.pid+'ORCID', 'propertyID', self.orcid, self.__original_orcid)


        super().save(*args, **kwargs)
        self.__original_email = self.email
        self.__original_first_name = self.first_name
        self.__original_last_name = self.last_name
        self.__original_orcid = self.orcid


    def __str__(self):
        return self.pid

@receiver(pre_delete, sender=User)
def delete_in_sparql(sender, instance, using, **kwargs):
    variables.sparql_generic_post_object.delete_subject(str(instance))
    variables.sparql_generic_post_object.delete_object(str(instance))
    variables.sparql_generic_post_object.delete_subject(str(instance)+"ARK")
    variables.sparql_generic_post_object.delete_object(str(instance)+"ARK")


class Title(models.Model):
    """
    Create a table in the database that will contain all the honorific prefix accessible by the users
    """
    title = models.CharField(max_length=50)

    __original_title = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_title = self.title

    def save(self, *args, **kwargs):

        if self.title != self.__original_title:
            variables.sparql_post_person_object.update_person_string_leaf_without_pid('honorificPrefix', self.title,
                                                                    self.__original_title)

        super().save(*args, **kwargs)
        self.__original_title = self.title


    def __str__(self):
        return self.title


class JobTitle(models.Model):
    """
    Create a table in the database that will contain all the job titles available by the users
    """
    job_title = models.CharField(max_length=100)

    __original_job_title = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_job_title = self.job_title

    def save(self, *args, **kwargs):

        if self.job_title != self.__original_job_title:
            variables.sparql_post_person_object.update_person_string_leaf_without_pid('jobTitle', self.job_title,
                                                                    self.__original_job_title)

        super().save(*args, **kwargs)
        self.__original_job_title = self.job_title


    def __str__(self):
        return self.job_title