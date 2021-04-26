from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST

class Sparql_post_Person_methods:
    """
    A class used to do sparql POST requests to the triplestore

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

    def init_person(self, ark_id, given_name, family_name):

        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_id}> a schema:Person ;
                    schema:givenName '{given_name}' ;
                    schema:familyName '{family_name}' ;
                    schema:email '' ;
                    schema:telephone '' ;
                    schema:description '' .
            }}
        """.format(prefix=self.prefix, ark_id=ark_id, given_name=given_name, family_name=family_name)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

if __name__ == "__main__":
    sparql = Sparql_post_Person_methods()
    print(sparql.init_person("ark/0000", "David", "nogueiras"))
