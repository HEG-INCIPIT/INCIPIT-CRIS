from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_institution import *
from .. import variables


class SparqlGetFunderMethods:
    """
    A class used to do sparql GET requests about funders to the triplestore.
    Funders are Institutions that have the type FundingScheme.

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


    def get_funders(self):
        """
        Get basic information of a funder : ark, name,
        And return a list for each funder
        """

        sparql_request = """
            {prefix}

            SELECT ?institution ?name ?alternateName WHERE
            {{
                ?institution a schema:FundingScheme .
                ?institution schema:name ?name .
                ?institution schema:alternateName ?alternateName .
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        return parse_get_institutions(self.sparql.query().response.read())


    def check_funder_ark(self, pid):
        """
        Return a boolean
        """

        sparql_request = """
            {prefix}

            SELECT ?fundingScheme WHERE
            {{
                <{ark_research}> a ?fundingScheme .
                FILTER(?fundingScheme = schema:FundingScheme)
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)
        return parse_check_institution_ark(self.sparql.query().response.read())


    def get_projects_funder(self, pid):
        """
        Get all the projects of the institution for who the creators were working for
        Return a dictionnary
        """

        sparql_request = """
            {prefix}

            SELECT ?project WHERE
            {{
                ?project schema:funder <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        projects = parse_get_projects_institution(self.sparql.query().response.read())

        projects_sorted = []
        for project in projects:
            projects_sorted.append(variables.sparql_get_project_object.get_minimum_data_project(project))
        projects_sorted.sort(key=lambda item: item['founding_date'], reverse=True)

        return projects_sorted
