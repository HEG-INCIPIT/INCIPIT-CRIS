from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST
from .. import variables


class SparqlPostSearchMethods:
    """
    A class used to do sparql POST requests about an Institution to the triplestore

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
        self.sparql.setMethod(POST)


    def search(self, query):
        sparql_request = query
        self.sparql.setQuery(sparql_request)
        return self.sparql.query().response.read()
