from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST
from .. import variables


class SparqlPostFunderMethods:
    """
    A class used to do sparql POST requests about a Funder to the triplestore

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


    def define_institution_funder(self, pid):
        """
        Attributes to a pid the class FundingScheme
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> a schema:FundingScheme .

            }}
        """.format(prefix=variables.prefix, pid=pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_institution_funder(self, pid):
        """
        Deletes the class FundingScheme from a pid's funder
        """
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> a schema:FundingScheme .

            }}
            WHERE
            {{
                <{pid}> a schema:FundingScheme .
            }}
        """.format(prefix=variables.prefix, pid=pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_project_to_funder(self, pid, project):
        """
        Adds a project to the given funder using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{project}> schema:funder <{pid}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, project=project)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_project_from_funder(self, pid, project):
        """
        Deletes a project from the given funder using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            DELETE {{
                <{project}> schema:funder <{pid}> .

            }}
            WHERE
            {{
                <{project}> schema:funder <{pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, project=project)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()
