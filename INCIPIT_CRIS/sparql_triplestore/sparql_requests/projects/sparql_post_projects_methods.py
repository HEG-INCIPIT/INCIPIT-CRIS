from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST
from .. import variables


class SparqlPostProjectsMethods:
    """
    A class used to do sparql POST requests about an Article to the triplestore

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

    def create_project(self, ark_pid, name, description, founding_date, dissolution_date, url):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{ark_pid}" .

                <{ark_pid}> a schema:ResearchProject ;
                    schema:name \"\"\"{name}\"\"\" ;
                    schema:description \"\"\"{description}\"\"\" ;
                    schema:foundingDate "{founding_date}"^^xsd:date ;
                    schema:dissolutionDate "{dissolution_date}"^^xsd:date ;
                    schema:url \"\"\"{url}\"\"\" ;
                    schema:identifier <{ark_pid}ARK> .
            }}
        """.format(prefix=variables.prefix, ark_pid=ark_pid, name=name, description=description, founding_date=founding_date, dissolution_date=dissolution_date, url=url)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def add_member_to_project(self, ark_pid, member):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_pid}> schema:member <{member}> .
            }}
        """.format(prefix=variables.prefix, ark_pid=ark_pid, member=member)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def delete_member_of_project(self, ark_pid, member):
        sparql_request = """
            {prefix}

            DELETE {{
                <{ark_pid}> schema:member <{member}> .

            }}
            WHERE
            {{
                <{ark_pid}> schema:member <{member}> .
            }}
        """.format(prefix=variables.prefix, ark_pid=ark_pid, member=member)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def delete_project(self, ark_pid):
        sparql_request = """
            {prefix}

            DELETE WHERE {{
                <{ark_pid}> ?predicate ?object .
            }}
        """.format(prefix=variables.prefix, ark_pid=ark_pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()
