from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST

class Sparql_post_Person_methods:
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

    url_endpoint = 'http://localhost:3030/INCIPIT-CRIS/'
    prefix = """
        PREFIX schema: <https://schema.org/>
    """
    admin = 'admin'
    password = 'pw'

    def __init__(self):

        self.sparql = SPARQLWrapper(self.url_endpoint)

        self.sparql.setHTTPAuth(DIGEST)
        self.sparql.setCredentials(self.admin, self.password)
        self.sparql.setReturnFormat(JSON)
        self.sparql.setMethod(POST)

    def init_person(self, ark_id, given_name, family_name, email):

        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_id}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{ark_id}" .
                
                <{ark_id}> a schema:Person ;
                    schema:givenName "{given_name}" ;
                    schema:familyName "{family_name}" ;
                    schema:email "{email}" ;
                    schema:description \"\"\"\"\"\";
                    schema:telephone \"\"\"\"\"\";
                    schema:identifier <{ark_id}ARK> .
            }}
        """.format(prefix=self.prefix, ark_id=ark_id, given_name=given_name, family_name=family_name, email=email)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def update_person_string_leaf(self, ark_id, predicat, new_string, old_string):

        sparql_request = """
            {prefix}

            DELETE {{ <{ark_id}> schema:{predicat} \"\"\"{old_string}\"\"\" }}
            INSERT {{ <{ark_id}> schema:{predicat} \"\"\"{new_string}\"\"\" }}
            WHERE
            {{
                <{ark_id}> schema:{predicat} \"\"\"{old_string}\"\"\"
            }}

        """.format(prefix=self.prefix, ark_id=ark_id, predicat=predicat, old_string=old_string, new_string=new_string)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()