from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from ..triplestore_JSON_responses_parser import Triplestore_JSON_responses_parser

class Sparql_get_Person_methods:
    """
    A class used to do sparql GET requests to the triplestore

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

    def get_persons(self):
        """
        Get information of persons : ark, given name, family name
        And return a list for each person
        """

        sparql_request = """
            {prefix}

            SELECT ?person ?given_name ?family_name WHERE
            {{
                ?person a schema:Person .
                ?person schema:givenName ?given_name .
                ?person schema:familyName ?family_name .
            }}
        """.format(prefix=self.prefix)

        self.sparql.setQuery(sparql_request)

        return Triplestore_JSON_responses_parser.parse_get_persons(self.sparql.query().response.read())

    def check_person_ark(self, ark_pid):
        """
        Return a boolean
        """

        sparql_request = """
            {prefix}

            SELECT ?person WHERE
            {{
                <{ark_research}> a ?person .
                FILTER(?person = schema:Person)
            }}
        """.format(prefix=self.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)
        return Triplestore_JSON_responses_parser.parse_check_person_ark(self.sparql.query().response.read())
