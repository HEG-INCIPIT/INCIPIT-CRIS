from .forms import *

def form_selection(request, field_to_edit, data):
    '''
    Select and return the correct form to be used in order to modify a field.

    Parameters
    ----------
    request : HttpRequest
        It is the metadata of the request.
    field_to_edit : String
        Indicates the field that is asked to be modified.
    data : Dictionary
        Contain the data of the different fields to be displayed on form before any modification.

    Returns
    -------
    Form
        A form with the field(s) desired
    '''

    # Check the request method
    if request.method == 'POST':
        if field_to_edit == 'name':
            return NameForm(request.POST)
        elif field_to_edit == 'alternateName':
            return AlternateNameForm(request.POST)
        elif field_to_edit == 'abstract':
            return AbstractForm(request.POST)
        elif field_to_edit == 'description':
            return DescriptionForm(request.POST)
        elif field_to_edit == 'telephone':
            return TelephoneForm(request.POST)
        
        # Form date
        elif field_to_edit == 'foundingDate':
            return ProjectFoundingDateForm(request.POST)
        elif field_to_edit == 'dissolutionDate':
            return ProjectDissolutionDateForm(request.POST)
        elif field_to_edit == 'datePublished':
            return ArticleDatePublishedForm(request.POST)
        elif field_to_edit == 'dateCreated':
            return DatasetCreatedDateForm(request.POST)
        elif field_to_edit == 'dateModified':
            return DatasetModifiedDateForm(request.POST)
        
        # Form url
        elif field_to_edit == 'url-details':
            return DatasetURLDetailsForm(request.POST)
        elif field_to_edit == 'url-data-download':
            return DatasetURLDataForm(request.POST)
        elif field_to_edit == 'url':
            return URLForm(request.POST)
        elif field_to_edit == 'logo':
            return URLForm(request.POST)

    # if not a POST it'll create a blank form
    else:
        if field_to_edit == 'name':
            return NameForm(old_name=data[field_to_edit])
        elif field_to_edit == 'alternateName':
            return AlternateNameForm(old_alternate_name=data['alternate_name'])
        elif field_to_edit == 'abstract':
            return AbstractForm(old_abstract=data[field_to_edit])
        elif field_to_edit == 'description':
            return DescriptionForm(old_description=data[field_to_edit])
        elif field_to_edit == 'telephone':
            return TelephoneForm(old_telephone=data[field_to_edit])
        
        # Form date
        elif field_to_edit == 'foundingDate':
            return ProjectFoundingDateForm(old_founding_date=data['founding_date'])
        elif field_to_edit == 'dissolutionDate':
            return ProjectDissolutionDateForm(old_dissolution_date=data['dissolution_date'])
        elif field_to_edit == 'datePublished':
            return ArticleDatePublishedForm(old_date_published=data['date_published'])
        elif field_to_edit == 'dateCreated':
            return DatasetCreatedDateForm(old_created_date=data['created_date'])
        elif field_to_edit == 'dateModified':
            return DatasetModifiedDateForm(old_modified_date=data['modified_date'])
        
        # Form url
        elif field_to_edit == 'url-details':
            return DatasetURLDetailsForm(old_url_details=data['url'])
        elif field_to_edit == 'url-data-download':
            return DatasetURLDataForm(old_url_data=data['data_download']['url'])
        elif field_to_edit == 'url':
            return URLForm(old_url=data['url'])
        elif field_to_edit == 'logo':
            return URLForm(old_url=data['logo'])
