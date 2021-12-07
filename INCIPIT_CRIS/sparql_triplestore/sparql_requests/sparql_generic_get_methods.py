from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST, TURTLE
from . import variables


class SparqlGenericGetMethods:
    """
    A class used to do generics sparql GET requests to the triplestore

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

    

    def __init__(self):
        self.sparql = SPARQLWrapper(variables.url_endpoint)

        self.sparql.setHTTPAuth(DIGEST)
        self.sparql.setCredentials(variables.admin, variables.password)
        self.sparql.setReturnFormat(JSON)
        self.sparql.setMethod(GET)

    def generate_backup(self):
        sparql_request = """
            CONSTRUCT   { ?subject ?predicate ?object }
            WHERE   { ?subject ?predicate ?object }
        """

        self.sparql.setQuery(sparql_request)

        self.sparql.setReturnFormat(TURTLE)

        results = self.sparql.query().convert()

        return results
