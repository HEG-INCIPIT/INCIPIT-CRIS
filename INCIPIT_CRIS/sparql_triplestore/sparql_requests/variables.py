from .article.sparql_get_article_methods import SparqlGetArticleMethods
from .person.sparql_get_person_methods import SparqlGetPersonMethods
from .project.sparql_get_project_methods import SparqlGetProjectMethods


url_endpoint = 'http://localhost:3030/INCIPIT-CRIS/'
prefix = """
    PREFIX schema: <https://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""
admin = 'admin'
password = 'pw'

sparql_get_article_object = SparqlGetArticleMethods()
sparql_get_person_object = SparqlGetPersonMethods()
sparql_get_project_object = SparqlGetProjectMethods()