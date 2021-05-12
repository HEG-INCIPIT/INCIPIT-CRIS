from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_responses_parser import Triplestore_JSON_responses_parser


class Sparql_get_articles_methods:
    """
    A class used to do sparql GET requests about a Person to the triplestore

    Attributes
    ----------
    url_endpoint : str
        the URL of the triplestore endpoint to do sparql resquests
    prefix : str
        the prefix of the ontologies used
    admin : str
        the username of the endpoint used
    password : str
        the password of the username used for access to the endpoint
    sparql : SPARQLWrapper
        an object to set connection to the triple store, choose return format of the triple store answers and the method used

    Methods
    -------

    """

    url_endpoint = 'http://localhost:3030/INCIPIT-CRIS/'
    prefix = """
        PREFIX schema: <https://schema.org/>
    """
    admin = 'admin'
    password = 'pw'

    def __init__(self):

        self.sparql = SPARQLWrapper(self.url_endpoint)

        self.sparql.setHTTPAuth(DIGEST)
        self.sparql.setCredentials(self.admin, self.password)
        self.sparql.setReturnFormat(JSON)
        self.sparql.setMethod(GET)

    def get_articles(self):
        """
        Get basic information of an article : ark, name,
        And return a list for each article
        """

        sparql_request = """
            {prefix}

            SELECT ?article ?name WHERE
            {{
                ?article a schema:ScholarlyArticle .
                ?article schema:name ?name .
            }}
        """.format(prefix=self.prefix)

        self.sparql.setQuery(sparql_request)

        return Triplestore_JSON_responses_parser.parse_get_articles(self.sparql.query().response.read())

