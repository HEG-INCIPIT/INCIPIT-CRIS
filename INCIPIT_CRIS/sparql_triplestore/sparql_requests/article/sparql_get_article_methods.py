from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_article import *
from .. import variables


class SparqlGetArticleMethods:
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


    def __init__(self):

        self.sparql = SPARQLWrapper(variables.url_endpoint)

        self.sparql.setHTTPAuth(DIGEST)
        self.sparql.setCredentials(variables.admin, variables.password)
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
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        return parse_get_articles(self.sparql.query().response.read())

    def get_authors_article(self, ark_pid):
        """
        Get all the authors of an article
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?author WHERE
            {{
                <{ark_research}> schema:author ?author .
            }}
        """.format(prefix=variables.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)

        array_authors = []

        for author in parse_get_authors_article(self.sparql.query().response.read()):
            full_name = variables.sparql_get_person_object.get_full_name_person(author)
            array_authors.append([author, full_name])

        return array_authors

    def get_data_article(self, ark_pid):
        """
        Get all the information of an article : ark, name, abstract, date of publication, authors, ...
        And return a dictionnary with all elements
        """

        sparql_request = """
            {prefix}

            SELECT ?name ?abstract ?datePublished ?url WHERE
            {{
                <{ark_research}> schema:name ?name .
                <{ark_research}> schema:abstract ?abstract .
                <{ark_research}> schema:datePublished ?datePublished .
                <{ark_research}> schema:url ?url .
            }}
        """.format(prefix=variables.prefix, ark_research=ark_pid)

        print(sparql_request)

        self.sparql.setQuery(sparql_request)

        data_article = parse_get_data_article(self.sparql.query().response.read())

        authors = variables.sparql_get_article_object.get_authors_article(ark_pid)
        
        data_article['authors'] = authors
        data_article['ark_pid'] = ark_pid
        return data_article

    def check_article_ark(self, ark_pid):
        """
        Return a boolean
        """

        sparql_request = """
            {prefix}

            SELECT ?scholarlyArticle WHERE
            {{
                <{ark_research}> a ?scholarlyArticle .
                FILTER(?scholarlyArticle = schema:ScholarlyArticle)
            }}
        """.format(prefix=variables.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)
        return parse_check_article_ark(self.sparql.query().response.read())
