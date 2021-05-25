from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST

class Sparql_generic_post_methods:
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

    url_endpoint = 'http://localhost:3030/INCIPIT-CRIS/'
    prefix = """
        PREFIX schema: <https://schema.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    """
    admin = 'admin'
    password = 'pw'

    def __init__(self):

        self.sparql = SPARQLWrapper(self.url_endpoint)

        self.sparql.setHTTPAuth(DIGEST)
        self.sparql.setCredentials(self.admin, self.password)
        self.sparql.setReturnFormat(JSON)
        self.sparql.setMethod(POST)

    def update_string_leaf(self, ark_pid, predicat, new_string, old_string):

        sparql_request = """
            {prefix}

            DELETE {{ <{ark_pid}> schema:{predicat} \"\"\"{old_string}\"\"\" }}
            INSERT {{ <{ark_pid}> schema:{predicat} \"\"\"{new_string}\"\"\" }}
            WHERE
            {{
                <{ark_pid}> schema:{predicat} \"\"\"{old_string}\"\"\"
            }}

        """.format(prefix=self.prefix, ark_pid=ark_pid, predicat=predicat, old_string=old_string, new_string=new_string)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def update_date_leaf(self, ark_pid, predicat, new_date, old_date):

        sparql_request = """
            {prefix}

            DELETE {{ <{ark_pid}> schema:{predicat} \"\"\"{old_date}\"\"\"^^xsd:date }}
            INSERT {{ <{ark_pid}> schema:{predicat} \"\"\"{new_date}\"\"\"^^xsd:date }}
            WHERE
            {{
                <{ark_pid}> schema:{predicat} \"\"\"{old_date}\"\"\"^^xsd:date
            }}

        """.format(prefix=self.prefix, ark_pid=ark_pid, predicat=predicat, old_date=old_date, new_date=new_date)

        print(sparql_request)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()