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

    def init_person(self, pid, given_name, family_name, email):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{pid}" .
                
                <{pid}> a schema:Person ;
                    schema:givenName "{given_name}" ;
                    schema:familyName "{family_name}" ;
                    schema:email "{email}" ;
                    schema:description \"\"\"\"\"\";
                    schema:telephone \"\"\"\"\"\";
                    schema:identifier <{pid}ARK> .
            }}
        """.format(prefix=variables.prefix, pid=pid, given_name=given_name, family_name=family_name, email=email)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_work_person(self, pid, work_pid):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:worksFor <{work_pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid , work_pid=work_pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    
    def delete_work_person(self, pid, work_pid):
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:worksFor <{work_pid}> .
            }}
            WHERE {{
                <{pid}> schema:worksFor <{work_pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid , work_pid=work_pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_affiliation_person(self, pid, affiliation_pid):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:affiliation <{affiliation_pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid , affiliation_pid=affiliation_pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    
    def delete_affiliation_person(self, pid, affiliation_pid):
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:affiliation <{affiliation_pid}> .
            }}
            WHERE {{
                <{pid}> schema:affiliation <{affiliation_pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid , affiliation_pid=affiliation_pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    
    def add_IN_information_person(self, pid, url):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}IN> a schema:PropertyValue ;
                    schema:name 'IN' ;
                    schema:url "{url}" .
                
                <{pid}> schema:identifier <{pid}IN> .
            }}
        """.format(prefix=variables.prefix, pid=pid, url=url)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def update_person_string_leaf(self, pid, predicate, new_string, old_string):
        sparql_request = """
            {prefix}

            DELETE {{ <{pid}> schema:{predicate} \"\"\"{old_string}\"\"\" }}
            INSERT {{ <{pid}> schema:{predicate} \"\"\"{new_string}\"\"\" }}
            WHERE
            {{
                <{pid}> schema:{predicate} \"\"\"{old_string}\"\"\"
            }}

        """.format(prefix=variables.prefix, pid=pid, predicate=predicate, old_string=old_string, new_string=new_string)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()
