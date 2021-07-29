from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST
from . import variables


class SparqlGenericPostMethods:
    """
    A class used to do generics sparql POST requests to the triplestore

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

    def update_string_leaf(self, pid, predicate, new_string, old_string):
        sparql_request = """
            {prefix}

            DELETE {{ <{pid}> schema:{predicate} \"\"\"{old_string}\"\"\" }}
            INSERT {{ <{pid}> schema:{predicate} \"\"\"{new_string}\"\"\" }}
            WHERE
            {{
                <{pid}> schema:{predicate} \"\"\"{old_string}\"\"\"
            }}

        """.format(prefix=variables.prefix, pid=pid, predicate=predicate, old_string=old_string,
                   new_string=new_string)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def update_date_leaf(self, pid, predicate, new_date, old_date):
        sparql_request = """
            {prefix}

            DELETE {{ <{pid}> schema:{predicate} \"\"\"{old_date}\"\"\"^^xsd:date }}
            INSERT {{ <{pid}> schema:{predicate} \"\"\"{new_date}\"\"\"^^xsd:date }}
            WHERE
            {{
                <{pid}> schema:{predicate} \"\"\"{old_date}\"\"\"^^xsd:date
            }}

        """.format(prefix=variables.prefix, pid=pid, predicate=predicate, old_date=old_date, new_date=new_date)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_subject(self, pid):
        sparql_request = """
            {prefix}

            DELETE WHERE {{
                <{pid}> ?predicate ?object .

            }}
        """.format(prefix=variables.prefix, pid=pid)

        self.sparql.setQuery(sparql_request)

        sparql_request = """
            {prefix}

            DELETE WHERE {{
                ?subject ?predicate <{pid}> .

            }}
        """.format(prefix=variables.prefix, pid=pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()