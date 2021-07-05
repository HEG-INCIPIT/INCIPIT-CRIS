from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_dataset import *
from .. import variables


class SparqlGetDatasetMethods:
    """
    A class used to do sparql GET requests about a dataset to the triplestore

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


    def get_datasets(self):
        """
        Get basic information of a dataset : ark, name,
        And return a list for each dataset
        """

        sparql_request = """
            {prefix}

            SELECT ?dataset ?name WHERE
            {{
                ?dataset a schema:Dataset .
                ?dataset schema:name ?name .
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        return parse_get_datasets(self.sparql.query().response.read())


    def get_full_name_dataset(self, ark_pid):
        """
        Get the name of an dataset formated in a dict
        Return a dict with name
        """
        sparql_request = """
            {prefix}

            SELECT ?name WHERE
            {{
                <{ark_research}> schema:name ?name .
            }}
        """.format(prefix=variables.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_full_name_dataset(self.sparql.query().response.read())


    def get_authors_dataset(self, ark_pid):
        """
        Get all the authors of an dataset
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

        for author in parse_get_authors_dataset(self.sparql.query().response.read()):
            full_name = variables.sparql_get_person_object.get_full_name_person(author)
            array_authors.append([author, full_name])

        return array_authors


    def get_projects_dataset(self, ark_pid):
        """
        Get all the projects of an dataset
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?project WHERE
            {{
                ?project schema:subjectOf <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=ark_pid)

        self.sparql.setQuery(sparql_request)

        array_projects = []

        for project in parse_get_projects_dataset(self.sparql.query().response.read()):
            name = variables.sparql_get_project_object.get_full_name_project(project)
            array_projects.append([project, name])

        return array_projects


    def get_data_dataset(self, ark_pid):
        """
        Get all the information of an dataset : ark, name, abstract, date of publication, authors, ...
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

        self.sparql.setQuery(sparql_request)

        data_dataset = parse_get_data_dataset(self.sparql.query().response.read())

        authors = variables.sparql_get_dataset_object.get_authors_dataset(ark_pid)
        projects = variables.sparql_get_dataset_object.get_projects_dataset(ark_pid)
        
        data_dataset['authors'] = authors
        data_dataset['projects'] = projects
        data_dataset['ark_pid'] = ark_pid
        return data_dataset

    def check_dataset_ark(self, ark_pid):
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
        return parse_check_dataset_ark(self.sparql.query().response.read())