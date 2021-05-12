from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST

class Sparql_post_articles_methods:
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

    def create_article(self, ark_pid, name, abstract, datePublished, creator):

        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{ark_pid}" .

                <{ark_pid}> a schema:ScholarlyArticle ;
                    schema:name \"\"\"{name}\"\"\" ;
                    schema:abstract \"\"\"{abstract}\"\"\" ;
                    schema:datePublished "{datePublished}"^^xsd:date ;
                    schema:author <{creator}> ;
                    schema:identifier <{ark_pid}ARK> .

            }}
        """.format(prefix=self.prefix, ark_pid=ark_pid, name=name, abstract=abstract, datePublished=datePublished, creator=creator)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()