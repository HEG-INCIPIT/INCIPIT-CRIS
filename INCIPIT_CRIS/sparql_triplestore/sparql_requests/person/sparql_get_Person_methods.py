from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_person import *


class SparqlGetPersonMethods:
    """
    A class used to do sparql GET requests about a Person to the triplestore

    Attributes
    ----------
    @url_endpoint : str
        the URL of the triplestore endpoint to do sparql resquests
    @prefix : str
        the prefix of the ontologies used
    @admin : str
        the username of the endpoint used
    @password : str
        the password of the username used for access to the endpoint
    @sparql : SPARQLWrapper
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
        Get basic information of persons : ark, given name, family name
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

        return parse_get_persons(self.sparql.query().response.read())

    def get_full_name_person(self, ark_pid):
        """
        Get the full name of a person format
        Return a dict with given name and family name
        """
        sparql_request = """
            {prefix}

            SELECT ?given_name ?family_name WHERE
            {{
                <{ark_research}> schema:givenName ?given_name .
                <{ark_research}> schema:familyName ?family_name .
            }}
        """.format(prefix=self.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_full_name_person(self.sparql.query().response.read())

    def get_articles_person(self, ark_pid):
        """
        Get all the articles for who the person is an author
        Return an array with tuples (identifier, dictionnary)
        """
        from ..articles.sparql_get_articles_methods import SparqlGetArticlesMethods

        sparql_request = """
            {prefix}

            SELECT ?article WHERE
            {{
                ?article schema:author <{ark_research}> .
            }}
        """.format(prefix=self.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)

        array_articles = []

        for article in parse_get_articles_person(self.sparql.query().response.read()):
            data_article = SparqlGetArticlesMethods().get_data_article(article)
            array_articles.append((article, data_article))

        return array_articles

    def get_data_person(self, ark_pid):
        """
        Get all the information of a person : ark, given name, family name, ...
        Return a dictionnary with all elements
        """

        sparql_request = """
            {prefix}

            SELECT ?given_name ?family_name ?email ?telephone ?description WHERE
            {{
                <{ark_research}> schema:givenName ?given_name .
                <{ark_research}> schema:familyName ?family_name .
                OPTIONAL {{ <{ark_research}> schema:email ?email }}
                OPTIONAL {{ <{ark_research}> schema:telephone ?telephone }}
                OPTIONAL {{ <{ark_research}> schema:description ?description }}
            }}
        """.format(prefix=self.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)

        articles = SparqlGetPersonMethods().get_articles_person(ark_pid)
        data_person = parse_get_data_person(self.sparql.query().response.read())
        data_person['articles'] = articles

        return data_person

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
        return parse_check_person_ark(self.sparql.query().response.read())
