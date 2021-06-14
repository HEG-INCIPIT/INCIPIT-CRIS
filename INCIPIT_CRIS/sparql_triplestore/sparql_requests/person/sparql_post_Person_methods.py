from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST
from .. import variables


class SparqlPostPersonMethods:
    """
    A class used to do sparql POST requests about a Person to the triplestore

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

    def init_person(self, ark_pid, given_name, family_name, email):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{ark_pid}" .
                
                <{ark_pid}> a schema:Person ;
                    schema:givenName "{given_name}" ;
                    schema:familyName "{family_name}" ;
                    schema:email "{email}" ;
                    schema:description \"\"\"\"\"\";
                    schema:telephone \"\"\"\"\"\";
                    schema:identifier <{ark_pid}ARK> .
            }}
        """.format(prefix=variables.prefix, ark_pid=ark_pid, given_name=given_name, family_name=family_name, email=email)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def update_person_string_leaf(self, ark_pid, predicate, new_string, old_string):
        sparql_request = """
            {prefix}

            DELETE {{ <{ark_pid}> schema:{predicate} \"\"\"{old_string}\"\"\" }}
            INSERT {{ <{ark_pid}> schema:{predicate} \"\"\"{new_string}\"\"\" }}
            WHERE
            {{
                <{ark_pid}> schema:{predicate} \"\"\"{old_string}\"\"\"
            }}

        """.format(prefix=variables.prefix, ark_pid=ark_pid, predicat=predicate, old_string=old_string, new_string=new_string)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()
