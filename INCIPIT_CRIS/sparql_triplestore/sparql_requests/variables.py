from .article.sparql_get_article_methods import SparqlGetArticleMethods
from .person.sparql_get_person_methods import SparqlGetPersonMethods
from .project.sparql_get_project_methods import SparqlGetProjectMethods
from .dataset.sparql_get_dataset_methods import SparqlGetDatasetMethods
from .institution.sparql_get_institution_methods import SparqlGetInstitutionMethods
from .funder.sparql_get_funder_methods import SparqlGetFunderMethods
from django.conf import settings


url_endpoint = 'http://localhost:3030/INCIPIT-CRIS/'
prefix = """
    PREFIX schema: <https://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""
admin = settings.FUSEKI_USER
password = settings.FUSEKI_PASSWORD

sparql_get_article_object = SparqlGetArticleMethods()
sparql_get_person_object = SparqlGetPersonMethods()
sparql_get_project_object = SparqlGetProjectMethods()
sparql_get_dataset_object = SparqlGetDatasetMethods()
sparql_get_institution_object = SparqlGetInstitutionMethods()
sparql_get_funder_object = SparqlGetFunderMethods()
