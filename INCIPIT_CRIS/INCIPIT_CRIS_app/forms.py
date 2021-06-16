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
    description = forms.CharField(label='Description ', max_length=300, required=False, validators=[not_quotes_regex], widget=forms.Textarea(attrs={'placeholder': 'Ajoutez votre description'}))

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_description' in kwargs:
            my_arg = kwargs.pop('old_description')
        super().__init__(*args, **kwargs)
        self.fields['description'].initial = my_arg


class TelephoneForm(forms.Form):
    telephone = forms.CharField(label='Telephone ', max_length=18, required=False, validators=[number_phone_regex])

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
    name = forms.CharField(label='Titre ', max_length=200, required=True, validators=[not_quotes_regex], widget=forms.Textarea)
    abstract = forms.CharField(label='Abstract ', max_length=2500, required=False, validators=[not_quotes_regex], widget=forms.Textarea)
    ark_pid = forms.CharField(label='Ark ', max_length=100, required=False, validators=[not_quotes_regex],
                              help_text='''Indiqué l'ark de l'article s'il existe, sinon laissez le champs vide''')
    date_published = forms.DateTimeField(widget=DateInput, label='Date de publication ', required=True)
    url = forms.CharField(label="URL", max_length=150, required=True, validators=[not_quotes_regex])


class ArticleNameForm(forms.Form):
    name = forms.CharField(label='Titre ', max_length=200, required=True, validators=[not_quotes_regex], widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_name' in kwargs:
            my_arg = kwargs.pop('old_name')
        super().__init__(*args, **kwargs)
        self.fields['name'].initial = my_arg


class ArticleAbstractForm(forms.Form):
    abstract = forms.CharField(label='Abstract ', max_length=2500, required=False, validators=[not_quotes_regex], widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_abstract' in kwargs:
            my_arg = kwargs.pop('old_abstract')
        super().__init__(*args, **kwargs)
        self.fields['abstract'].initial = my_arg


class ArticleDatePublishedForm(forms.Form):
    date_published = forms.DateTimeField(widget=DateInput, label='Date de publication ', required=False)

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
    name = forms.CharField(label='Titre ', max_length=200, required=True, validators=[not_quotes_regex], widget=forms.Textarea)
    description = forms.CharField(label='Description ', max_length=2500, required=False, validators=[not_quotes_regex], widget=forms.Textarea)
    ark_pid = forms.CharField(label='Ark ', max_length=100, required=False, validators=[not_quotes_regex],
                              help_text='''Indiqué l'ark de l'article s'il existe, sinon laissez le champs vide''')
    founding_date = forms.DateTimeField(widget=DateInput, label='Date de début ', required=True)
    dissolution_date = forms.DateTimeField(widget=DateInput, label='Date de fin ', required=True)
    url = forms.CharField(label="URL", max_length=150, required=True, validators=[not_quotes_regex])


class ProjectNameForm(forms.Form):
    name = forms.CharField(label='Titre ', max_length=200, required=True, validators=[not_quotes_regex], widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_name' in kwargs:
            my_arg = kwargs.pop('old_name')
        super().__init__(*args, **kwargs)
        self.fields['name'].initial = my_arg


class ProjectDescriptionForm(forms.Form):
    description = forms.CharField(label='Description ', max_length=2500, required=False, validators=[not_quotes_regex], widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_description' in kwargs:
            my_arg = kwargs.pop('old_description')
        super().__init__(*args, **kwargs)
        self.fields['description'].initial = my_arg


class ProjectFoundingDateForm(forms.Form):
    founding_date = forms.DateTimeField(widget=DateInput, label='Date de début ', required=False)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_founding_date' in kwargs:
            my_arg = kwargs.pop('old_founding_date')
        super().__init__(*args, **kwargs)
        self.fields['founding_date'].initial = my_arg


class ProjectDissolutionDateForm(forms.Form):
    dissolution_date = forms.DateTimeField(widget=DateInput, label='Date de fin ', required=False)

    def __init__(self, *args, **kwargs):
        # overload init function to display actual value of the variable in this field
        my_arg = ''
        if 'old_dissolution_date' in kwargs:
            my_arg = kwargs.pop('old_dissolution_date')
        super().__init__(*args, **kwargs)
        self.fields['dissolution_date'].initial = my_arg