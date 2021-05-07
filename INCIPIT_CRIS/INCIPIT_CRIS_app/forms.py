from django import forms
from django.core.validators import RegexValidator

number_phone_regex = RegexValidator(r"^[0-9]*$", "Le numéro de téléphone doit contenir uniquement des chiffres")
description_regex = RegexValidator(r"""[^".{3,}]""", "Vous ne pouvez pas mettre trois guillemets de suite")

class DescriptionForm(forms.Form):
    url_post_redirect = "description"
    old_description = ""
    description = forms.CharField(label='Description ', max_length=300, required=False, validators=[description_regex])

    def __init__(self, *args, **kwargs):
        my_arg = ''
        if 'old_description' in kwargs:
            my_arg = kwargs.pop('old_description')
        super().__init__(*args, **kwargs)
        if my_arg != '':
            self.fields['description'].initial = my_arg

class TelephoneForm(forms.Form):
    url_post_redirect = "telephone"
    old_telephone = ""
    telephone = forms.CharField(label='Telephone ', max_length=18, required=False, validators=[number_phone_regex])

    def __init__(self, *args, **kwargs):
        my_arg = ''
        if 'old_telephone' in kwargs:
            my_arg = kwargs.pop('old_telephone')
        super().__init__(*args, **kwargs)
        if my_arg != '':
            self.fields['telephone'].initial = my_arg

