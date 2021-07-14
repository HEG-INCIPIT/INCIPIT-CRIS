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


    def get_full_name_dataset(self, pid):
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
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_full_name_dataset(self.sparql.query().response.read())


    def get_maintainers_dataset(self, pid):
        """
        Get all the maintainers of an dataset
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?maintainer WHERE
            {{
                <{ark_research}> schema:maintainer ?maintainer .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_maintainers = []

        for maintainer in parse_get_maintainers_dataset(self.sparql.query().response.read()):
            full_name = variables.sparql_get_person_object.get_full_name_person(maintainer)
            array_maintainers.append([maintainer, full_name])

        return array_maintainers


    def get_creators_dataset(self, pid):
        """
        Get all the creators of an dataset
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?creator WHERE
            {{
                <{ark_research}> schema:creator ?creator .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_creators = []

        for creator in parse_get_creators_dataset(self.sparql.query().response.read()):
            full_name = variables.sparql_get_person_object.get_full_name_person(creator)
            array_creators.append([creator, full_name])

        return array_creators


    def get_projects_dataset(self, pid):
        """
        Get all the projects of an dataset
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?project WHERE
            {{
                <{ark_research}> schema:producer ?project .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_projects = []

        for project in parse_get_projects_dataset(self.sparql.query().response.read()):
            name = variables.sparql_get_project_object.get_full_name_project(project)
            array_projects.append([project, name])

        return array_projects

    
    def get_articles_dataset(self, pid):
        """
        Get all the articles of an dataset
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?article WHERE
            {{
                ?article schema:producer <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_articles = []

        for article in parse_get_articles_dataset(self.sparql.query().response.read()):
            name = variables.sparql_get_article_object.get_full_name_article(article)
            array_articles.append([article, name])

        return array_articles


    def get_data_dataset(self, pid):
        """
        Get all the information of an dataset : ark, name, abstract, date of publication, maintainers, ...
        And return a dictionnary with all elements
        """

        sparql_request = """
            {prefix}

            SELECT ?name ?abstract ?dateCreated ?dateModified ?url WHERE
            {{
                <{ark_research}> schema:name ?name .
                <{ark_research}> schema:abstract ?abstract .
                <{ark_research}> schema:dateCreated ?dateCreated .
                <{ark_research}> schema:dateModified ?dateModified .
                <{ark_research}> schema:url ?url .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        data_dataset = parse_get_data_dataset(self.sparql.query().response.read())

        maintainers = variables.sparql_get_dataset_object.get_maintainers_dataset(pid)
        creators = variables.sparql_get_dataset_object.get_creators_dataset(pid)
        projects = variables.sparql_get_dataset_object.get_projects_dataset(pid)
        data_download = variables.sparql_get_dataset_object.get_data_download_dataset(pid)
        
        data_dataset['maintainers'] = maintainers
        data_dataset['creators'] = creators
        data_dataset['projects'] = projects
        data_dataset['pid'] = pid
        data_dataset['data_download'] = data_download
        return data_dataset

    def check_dataset_ark(self, pid):
        """
        Return a boolean
        """

        sparql_request = """
            {prefix}

            SELECT ?dataset WHERE
            {{
                <{ark_research}> a ?dataset .
                FILTER(?dataset = schema:Dataset)
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)
        return parse_check_dataset_ark(self.sparql.query().response.read())


    def get_data_download_dataset(self, pid):

        sparql_request = """
            {prefix}

            SELECT ?url WHERE
            {{
                <{ark_research}DD> schema:url ?url .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_data_download_dataset(self.sparql.query().response.read())