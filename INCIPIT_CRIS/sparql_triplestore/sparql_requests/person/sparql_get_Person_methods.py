from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_person import *
from .. import variables


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

    def __init__(self):
        self.sparql = SPARQLWrapper(variables.url_endpoint)

        self.sparql.setHTTPAuth(DIGEST)
        self.sparql.setCredentials(variables.admin, variables.password)
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
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        return parse_get_persons(self.sparql.query().response.read())

    def get_full_name_person(self, pid):
        """
        Get the full name of a person formated in a dict
        Return a dict with given name and family name
        """
        sparql_request = """
            {prefix}

            SELECT ?given_name ?family_name WHERE
            {{
                <{ark_research}> schema:givenName ?given_name .
                <{ark_research}> schema:familyName ?family_name .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_full_name_person(self.sparql.query().response.read())

    def get_articles_person(self, pid):
        """
        Get all the articles for who the person is an author
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?article WHERE
            {{
                ?article schema:author <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_articles = []

        for article in parse_get_articles_person(self.sparql.query().response.read()):
            data_article = variables.sparql_get_article_object.get_data_article(article)
            array_articles.append((article, data_article))

        return array_articles


    def get_projects_person(self, pid):
        """
        Get all the projects for who the person is a member
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?project WHERE
            {{
                ?project schema:member <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_projects = []

        for project in parse_get_projects_person(self.sparql.query().response.read()):
            data_project = variables.sparql_get_project_object.get_data_project(project)
            array_projects.append((project, data_project))

        return array_projects


    def get_datasets_creator_person(self, pid):
        """
        Get all the datasets for who the person is a creator
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?dataset WHERE
            {{
                ?dataset schema:creator <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_datasets = []

        for dataset in parse_get_datasets_person(self.sparql.query().response.read()):
            data_dataset = variables.sparql_get_dataset_object.get_data_dataset(dataset)
            array_datasets.append((dataset, data_dataset))

        return array_datasets


    def get_datasets_maintainer_person(self, pid):
        """
        Get all the datasets for who the person is a maintainer
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?dataset WHERE
            {{
                ?dataset schema:maintainer <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_datasets = []

        for dataset in parse_get_datasets_person(self.sparql.query().response.read()):
            data_dataset = variables.sparql_get_dataset_object.get_data_dataset(dataset)
            array_datasets.append((dataset, data_dataset))

        return array_datasets


    def get_data_person(self, pid):
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
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        data_person = parse_get_data_person(self.sparql.query().response.read())

        articles = variables.sparql_get_person_object.get_articles_person(pid)
        projects = variables.sparql_get_person_object.get_projects_person(pid)
        datasets_creator = variables.sparql_get_person_object.get_datasets_creator_person(pid)
        datasets_maintainer = variables.sparql_get_person_object.get_datasets_maintainer_person(pid)
        
        data_person['pid'] = pid
        data_person['articles'] = articles
        data_person['projects'] = projects
        data_person['datasets_creator'] = datasets_creator
        data_person['datasets_maintainer'] = datasets_maintainer

        return data_person

    def check_person_ark(self, pid):
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
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)
        return parse_check_person_ark(self.sparql.query().response.read())
