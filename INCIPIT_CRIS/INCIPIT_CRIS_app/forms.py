from django import forms
from django.core.validators import RegexValidator

not_quotes_regex = RegexValidator(r"""[^".{3,}]""", "Vous ne pouvez pas mettre trois guillemets de suite")

class DateInput(forms.DateInput):
    input_type = 'date'

##################################################
# Person forms
##################################################

number_phone_regex = RegexValidator(r"^[0-9]*$", "Le numéro de téléphone doit contenir uniquement des chiffres")

class DescriptionForm(forms.Form):
    description = forms.CharField(label='Description ', max_length=300, required=False, validators=[not_quotes_regex])

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value for a field in this one
        my_arg = ''
        if 'old_description' in kwargs:
            my_arg = kwargs.pop('old_description')
        super().__init__(*args, **kwargs)
        self.fields['description'].initial = my_arg

class TelephoneForm(forms.Form):
    telephone = forms.CharField(label='Telephone ', max_length=18, required=False, validators=[number_phone_regex])

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value for a field in this one
        my_arg = ''
        if 'old_telephone' in kwargs:
            my_arg = kwargs.pop('old_telephone')
        super().__init__(*args, **kwargs)
        self.fields['telephone'].initial = my_arg


##################################################
# Articles forms
##################################################

class ArticleCreationForm(forms.Form):
    name = forms.CharField(label='Titre ', max_length=200, required=True, validators=[not_quotes_regex])
    abstract = forms.CharField(label='Abstract ', max_length=1500, required=False, validators=[not_quotes_regex])
    ark_pid = forms.CharField(label='Ark ', max_length=100, required=False, validators=[not_quotes_regex], help_text='''Indiqué l'ark de l'article s'il existe, sinon laissez le champs vide''')
    date_published = forms.DateTimeField(widget=DateInput, label='Date de publication ', required=False)
    