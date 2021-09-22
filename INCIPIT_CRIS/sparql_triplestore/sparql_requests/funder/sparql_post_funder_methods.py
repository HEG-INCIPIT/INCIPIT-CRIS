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


    def define_funder(self, pid):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> a schema:FundingScheme .

            }}
        """.format(prefix=variables.prefix, pid=pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_funder(self, pid):
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
