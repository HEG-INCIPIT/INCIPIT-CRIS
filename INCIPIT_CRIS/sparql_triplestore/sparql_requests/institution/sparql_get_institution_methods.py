from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_institution import *
from .. import variables


class SparqlGetInstitutionMethods:
    """
    A class used to do sparql GET requests about institutions to the triplestore

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


    def get_institutions(self):
        """
        Get basic information of an institution : ark, name,
        And return a list for each institution
        """

        sparql_request = """
            {prefix}

            SELECT ?institution ?name WHERE
            {{
                ?institution a schema:ResearchOrganization .
                ?institution schema:name ?name .
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        return parse_get_institutions(self.sparql.query().response.read())


    def get_full_name_institution(self, pid):
        """
        Get the name of an institution formated in a dict
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

        return parse_get_full_name_institution(self.sparql.query().response.read())


    def get_projects_institution(self, pid):
        """
        Get all the projects of an institution
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?project WHERE
            {{
                ?project schema:subjectOf <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_projects = []

        for project in parse_get_projects_institution(self.sparql.query().response.read()):
            name = variables.sparql_get_project_object.get_full_name_project(project)
            array_projects.append([project, name])

        return array_projects


    def get_data_institution(self, pid):
        """
        Get all the information of an institution : ark, name, abstract, date of publication, authors, ...
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
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        data_institution = parse_get_data_institution(self.sparql.query().response.read())

        projects = variables.sparql_get_institution_object.get_projects_institution(pid)
        
        data_institution['projects'] = projects
        data_institution['pid'] = pid
        return data_institution


    def check_institution_ark(self, pid):
        """
        Return a boolean
        """

        sparql_request = """
            {prefix}

            SELECT ?researchOrganization WHERE
            {{
                <{ark_research}> a ?researchOrganization .
                FILTER(?researchOrganization = schema:ResearchOrganization)
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)
        return parse_check_institution_ark(self.sparql.query().response.read())
