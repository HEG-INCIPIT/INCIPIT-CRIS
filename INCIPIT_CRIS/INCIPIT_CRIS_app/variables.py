from arketype_API.ark import Ark
from sparql_triplestore.sparql_requests.sparql_generic_post_methods import SparqlGenericPostMethods
from sparql_triplestore.sparql_requests.person.sparql_get_Person_methods import SparqlGetPersonMethods
from sparql_triplestore.sparql_requests.articles.sparql_get_articles_methods import SparqlGetArticlesMethods
from sparql_triplestore.sparql_requests.articles.sparql_post_articles_methods import SparqlPostArticlesMethods
from sparql_triplestore.sparql_requests.projects.sparql_get_projects_methods import SparqlGetProjectsMethods
from sparql_triplestore.sparql_requests.projects.sparql_post_projects_methods import SparqlPostProjectsMethods


ark = Ark
sparql_generic_post_object = SparqlGenericPostMethods()
sparql_get_person_object = SparqlGetPersonMethods()
sparql_get_article_object = SparqlGetArticlesMethods()
sparql_post_article_object = SparqlPostArticlesMethods()
sparql_get_project_object = SparqlGetProjectsMethods()
sparql_post_project_object = SparqlPostProjectsMethods()