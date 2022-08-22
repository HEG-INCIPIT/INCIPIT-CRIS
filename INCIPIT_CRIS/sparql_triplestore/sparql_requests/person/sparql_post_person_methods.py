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
        """
        Create a person ressource
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}ARK> a schema:PropertyValue ;
                    schema:name 'ARK' ;
                    schema:propertyID "{pid}" .

                <{pid}ORCID> a schema:PropertyValue ;
                    schema:name 'ORCID' ;
                    schema:propertyID "" .
                
                <{pid}> a schema:Person ;
                    schema:givenName "{given_name}" ;
                    schema:familyName "{family_name}" ;
                    schema:email "{email}" ;
                    schema:description \"""\""";
                    schema:telephone \"""\""";
                    schema:address \"""\""";
                    schema:identifier <{pid}ARK> ;
                    schema:identifier <{pid}ORCID> .
            }}
        """.format(prefix=variables.prefix, pid=pid, given_name=given_name, family_name=family_name, email=email)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_work_person(self, pid, work_pid):
        """
        Adds an institution of work to the given person using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{work_pid}> schema:worksFor <{pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid , work_pid=work_pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    
    def delete_work_person(self, pid, work_pid):
        """
        Deletes an institution of work from the given person using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            DELETE {{
                <{work_pid}> schema:worksFor <{pid}> .
            }}
            WHERE {{
                <{work_pid}> schema:worksFor <{pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid , work_pid=work_pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_affiliation_person(self, pid, affiliation_pid):
        """
        Adds an institution of affiliation to the given person using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{affiliation_pid}> schema:affiliation <{pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid , affiliation_pid=affiliation_pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    
    def delete_affiliation_person(self, pid, affiliation_pid):
        """
        Deletes an institution of affiliation from the given person using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            DELETE {{
                <{affiliation_pid}> schema:affiliation <{pid}> .
            }}
            WHERE {{
                <{affiliation_pid}> schema:affiliation <{pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid , affiliation_pid=affiliation_pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_job_title_person(self, pid, job_title):
        """
        Adds a job title to the given person using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:jobTitle \"""{job_title}\""" .
            }}
        """.format(prefix=variables.prefix, pid=pid , job_title=job_title)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    
    def delete_job_title_person(self, pid, job_title):
        """
        Deletes a job title from the given person using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:jobTitle \"""{job_title}\""" .
            }}
            WHERE {{
                <{pid}> schema:jobTitle \"""{job_title}\""" .
            }}
        """.format(prefix=variables.prefix, pid=pid , job_title=job_title)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_title_person(self, pid, title):
        """
        Adds a honorific title to the given person using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:honorificPrefix \"""{title}\""" .
            }}
        """.format(prefix=variables.prefix, pid=pid , title=title)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    
    def delete_title_person(self, pid, title):
        """
        Deletes a honorific title from the given person using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:honorificPrefix \"""{title}\""" .
            }}
            WHERE {{
                <{pid}> schema:honorificPrefix \"""{title}\""" .
            }}
        """.format(prefix=variables.prefix, pid=pid , title=title)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    
    def add_IN_information_person(self, pid, url):
        """
        Adds a LinkedIn url to the given person using pid's for both ressources
        """
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


    def delete_IN_information_person(self, pid, url):
        """
        Deletes a LinkedIn url from the given person using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            DELETE WHERE {{
                <{pid}IN> a schema:PropertyValue ;
                    schema:name 'IN' ;
                    schema:url "{url}" .
                
                <{pid}> schema:identifier <{pid}IN> .
            }}
        """.format(prefix=variables.prefix, pid=pid, url=url)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def update_person_string_leaf(self, pid, predicate, new_string, old_string):
        """
        Updates the string of a predicates using the pid of the person
        """
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


    def update_person_string_leaf_without_pid(self, predicate, new_string, old_string):
        """
        Updates the string of a predicates without using the pid of the person
        """
        sparql_request = """
            {prefix}

            DELETE {{ ?person schema:{predicate} \"\"\"{old_string}\"\"\" }}
            INSERT {{ ?person schema:{predicate} \"\"\"{new_string}\"\"\" }}
            WHERE
            {{
                ?person schema:{predicate} \"\"\"{old_string}\"\"\"
            }}

        """.format(prefix=variables.prefix, predicate=predicate, old_string=old_string, new_string=new_string)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()
