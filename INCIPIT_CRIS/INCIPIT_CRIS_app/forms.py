from django import forms
from django.core.validators import RegexValidator
from django.forms.widgets import NumberInput

not_quotes_regex = RegexValidator(r"""[^".{3,}]""", "Vous ne pouvez pas mettre trois guillemets de suite")


class DateInput(forms.DateInput):
    input_type = 'date'


##################################################
# Person forms
##################################################

number_phone_regex = RegexValidator(r"^[0-9]*$", "Le numéro de téléphone doit contenir uniquement des chiffres")


class DescriptionForm(forms.Form):
    description = forms.CharField(label='Description ', max_length=300, required=False, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'placeholder': 'Ajoutez votre description', 'class':'textarea'}))

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_description' in kwargs:
            my_arg = kwargs.pop('old_description')
        super().__init__(*args, **kwargs)
        self.fields['description'].initial = my_arg


class TelephoneForm(forms.Form):
    telephone = forms.CharField(label='Téléphone ', max_length=18, required=False, validators=[number_phone_regex], widget=forms.TextInput(attrs={'placeholder': 'Numéro', 'class':'input'}))

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_telephone' in kwargs:
            my_arg = kwargs.pop('old_telephone')
        super().__init__(*args, **kwargs)
        self.fields['telephone'].initial = my_arg


##################################################
# Article forms
##################################################

class ArticleCreationForm(forms.Form):
    name = forms.CharField(label='Titre ', max_length=200, required=True, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'placeholder':'Nom', 'class':'textarea'}))
    abstract = forms.CharField(label='Abstract ', max_length=2500, required=False, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'placeholder':'Résumé', 'class':'textarea'}))
    ark_pid = forms.CharField(label='Ark ', max_length=100, required=False, validators=[not_quotes_regex],
                              help_text='''Indiqué l'ark de l'article s'il existe, sinon laissez le champs vide''', widget=forms.TextInput(attrs={'placeholder': 'Laisser vide pour créer automatiquement un ark', 'class':'input'}))
    date_published = forms.DateTimeField(widget=DateInput(attrs={'class':'input'}), label='Date de publication ', required=True)
    url = forms.CharField(label="URL", max_length=200, required=True, validators=[not_quotes_regex], widget=forms.TextInput(attrs={'placeholder': 'URL', 'class':'input'}))


class ArticleDatePublishedForm(forms.Form):
    date_published = forms.DateTimeField(widget=DateInput(attrs={'placeholder':'Date de publication', 'class':'input'}), label='Date de publication ', required=False)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_date_published' in kwargs:
            my_arg = kwargs.pop('old_date_published')
        super().__init__(*args, **kwargs)
        self.fields['date_published'].initial = my_arg


##################################################
# Project forms
##################################################

class ProjectCreationForm(forms.Form):
    name = forms.CharField(label='Titre ', max_length=200, required=True, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'placeholder':'Nom', 'class':'textarea'}))
    description = forms.CharField(label='Description ', max_length=2500, required=False, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'placeholder':'Description', 'class':'textarea'}))
    ark_pid = forms.CharField(label='Ark ', max_length=100, required=False, validators=[not_quotes_regex],
                              help_text='''Indiqué l'ark du projet s'il existe, sinon laissez le champs vide''', widget=forms.TextInput(attrs={'placeholder': 'Laisser vide pour créer automatiquement un ark', 'class':'input'}))
    founding_date = forms.DateTimeField(widget=DateInput(attrs={'class':'input'}), label='Date de début ', required=True)
    dissolution_date = forms.DateTimeField(widget=DateInput(attrs={'class':'input'}), label='Date de fin ', required=True)
    url = forms.CharField(label="URL", max_length=200, required=True, validators=[not_quotes_regex], widget=forms.TextInput(attrs={'placeholder': 'URL', 'class':'input'}))


class ProjectFoundingDateForm(forms.Form):
    founding_date = forms.DateTimeField(widget=DateInput(attrs={'class':'input'}), label='Date de début ', required=False)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_founding_date' in kwargs:
            my_arg = kwargs.pop('old_founding_date')
        super().__init__(*args, **kwargs)
        self.fields['founding_date'].initial = my_arg


class ProjectDissolutionDateForm(forms.Form):
    dissolution_date = forms.DateTimeField(widget=DateInput(attrs={'class':'input'}), label='Date de fin ', required=False)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_dissolution_date' in kwargs:
            my_arg = kwargs.pop('old_dissolution_date')
        super().__init__(*args, **kwargs)
        self.fields['dissolution_date'].initial = my_arg


##################################################
# Dataset forms
##################################################

class DatasetCreationForm(forms.Form):
    name = forms.CharField(label='Titre ', max_length=200, required=True, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'class':'textarea'}))
    abstract = forms.CharField(label='Abstract ', max_length=2500, required=False, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'class':'textarea'}))
    ark_pid = forms.CharField(label='Ark ', max_length=100, required=False, validators=[not_quotes_regex],
                              help_text='''Indiqué l'ark du jeu de données s'il existe, sinon laissez le champs vide''', widget=forms.TextInput(attrs={'placeholder': 'Laisser vide pour créer automatiquement un ark', 'class':'input'}))
    created_date = forms.DateTimeField(widget=DateInput(attrs={'class':'input'}), label='Date de création ', required=True)
    modified_date = forms.DateTimeField(widget=DateInput(attrs={'class':'input'}), label='Date de modification ', required=True)
    url_details = forms.CharField(label="URL", max_length=200, required=True, validators=[not_quotes_regex], widget=forms.TextInput(attrs={'placeholder': 'URL des détails', 'class':'input'}))
    url_data = forms.CharField(label="URL", max_length=200, required=True, validators=[not_quotes_regex], widget=forms.TextInput(attrs={'placeholder': 'URL des données', 'class':'input'}))


class DatasetCreatedDateForm(forms.Form):
    created_date = forms.DateTimeField(widget=DateInput(attrs={'class':'input'}), label='Date de création ', required=False)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_created_date' in kwargs:
            my_arg = kwargs.pop('old_created_date')
        super().__init__(*args, **kwargs)
        self.fields['created_date'].initial = my_arg


class DatasetModifiedDateForm(forms.Form):
    modified_date = forms.DateTimeField(widget=DateInput(attrs={'class':'input'}), label='Date de création ', required=False)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_modified_date' in kwargs:
            my_arg = kwargs.pop('old_modified_date')
        super().__init__(*args, **kwargs)
        self.fields['modified_date'].initial = my_arg


class DatasetURLDetailsForm(forms.Form):
    url_details = forms.CharField(label="URL", max_length=200, required=True, validators=[not_quotes_regex], widget=forms.TextInput(attrs={'placeholder': 'URL des détails', 'class':'input'}))

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_url_details' in kwargs:
            my_arg = kwargs.pop('old_url_details')
        super().__init__(*args, **kwargs)
        self.fields['url_details'].initial = my_arg


class DatasetURLDataForm(forms.Form):
    url_data = forms.CharField(label="URL", max_length=200, required=True, validators=[not_quotes_regex], widget=forms.TextInput(attrs={'placeholder': 'URL des données', 'class':'input'}))

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_url_data' in kwargs:
            my_arg = kwargs.pop('old_url_data')
        super().__init__(*args, **kwargs)
        self.fields['url_data'].initial = my_arg


##################################################
# Generic forms
##################################################


class URLForm(forms.Form):
    url = forms.CharField(label='Titre ', max_length=200, required=True, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'placeholder':'URL', 'class':'textarea'}))

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_url' in kwargs:
            my_arg = kwargs.pop('old_url')
        super().__init__(*args, **kwargs)
        self.fields['url'].initial = my_arg


class NameForm(forms.Form):
    name = forms.CharField(label='Titre ', max_length=200, required=True, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'placeholder':'Nom', 'class':'textarea'}))

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_name' in kwargs:
            my_arg = kwargs.pop('old_name')
        super().__init__(*args, **kwargs)
        self.fields['name'].initial = my_arg


class AbstractForm(forms.Form):
    abstract = forms.CharField(label='Abstract ', max_length=2500, required=False, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'placeholder':'Résumé', 'class':'textarea'}))

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_abstract' in kwargs:
            my_arg = kwargs.pop('old_abstract')
        super().__init__(*args, **kwargs)
        self.fields['abstract'].initial = my_arg
