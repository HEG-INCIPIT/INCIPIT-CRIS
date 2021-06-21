from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_project import *
from .. import variables


class SparqlGetProjectMethods:
    """
    A class used to do sparql GET requests about projects to the triplestore

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


    def get_projects(self):
        """
        Get basic information of a project : ark, name,
        And return a list for each project
        """

        sparql_request = """
            {prefix}

            SELECT ?project ?name WHERE
            {{
                ?project a schema:ResearchProject .
                ?project schema:name ?name .
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        return parse_get_projects(self.sparql.query().response.read())


    def get_members_project(self, ark_pid):
        """
        Get all the members of a project
        And return an array with tuples (identifier, dictionnary)
        """
        from ..person.sparql_get_person_methods import SparqlGetPersonMethods

        sparql_request = """
            {prefix}

            SELECT ?member WHERE
            {{
                <{ark_research}> schema:member ?member .
            }}
        """.format(prefix=variables.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)

        array_members = []

        for member in parse_get_members_project(self.sparql.query().response.read()):
            full_name = variables.sparql_get_person_object.get_full_name_person(member)
            array_members.append([member, full_name])

        return array_members


    def get_articles_project(self, ark_pid):
        """
        Get all the articles of a project
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?article WHERE
            {{
                <{ark_research}> schema:subjectOf ?article .
            }}
        """.format(prefix=variables.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)

        array_articles = []

        for article in parse_get_articles_project(self.sparql.query().response.read()):
            full_name = variables.sparql_get_article_object.get_full_name_article(article)
            array_articles.append([article, full_name])

        return array_articles


    def get_data_project(self, ark_pid):
        """
        Get all the information of a project : ark, name, abstract, date of publication, members, ...
        And return a dictionnary with all elements
        """
        sparql_request = """
            {prefix}

            SELECT ?name ?description ?foundingDate ?dissolutionDate ?url WHERE
            {{
                <{ark_research}> schema:name ?name .
                <{ark_research}> schema:description ?description .
                <{ark_research}> schema:foundingDate ?foundingDate .
                <{ark_research}> schema:dissolutionDate ?dissolutionDate .
                <{ark_research}> schema:url ?url .
            }}
        """.format(prefix=variables.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)
        data_project = parse_get_data_project(self.sparql.query().response.read())

        members = variables.sparql_get_project_object.get_members_project(ark_pid)
        articles = variables.sparql_get_project_object.get_articles_project(ark_pid)
        
        data_project['members'] = members
        data_project['articles'] = articles
        data_project['ark_pid'] = ark_pid
        return data_project


    def check_project_ark(self, ark_pid):
        """
        Return a boolean
        """

        sparql_request = """
            {prefix}

            SELECT ?researchProject WHERE
            {{
                <{ark_research}> a ?researchProject .
                FILTER(?researchProject = schema:ResearchProject)
            }}
        """.format(prefix=variables.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)
        return parse_check_project_ark(self.sparql.query().response.read())
