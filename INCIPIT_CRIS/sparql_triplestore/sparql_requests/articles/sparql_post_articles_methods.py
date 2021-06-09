from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST


class SparqlPostArticlesMethods:
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

    def create_article(self, ark_pid, name, abstract, date_published, url):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{ark_pid}" .

                <{ark_pid}> a schema:ScholarlyArticle ;
                    schema:name \"\"\"{name}\"\"\" ;
                    schema:abstract \"\"\"{abstract}\"\"\" ;
                    schema:datePublished "{date_published}"^^xsd:date ;
                    schema:url \"\"\"{url}\"\"\" ;
                    schema:identifier <{ark_pid}ARK> .

            }}
        """.format(prefix=self.prefix, ark_pid=ark_pid, name=name, abstract=abstract, date_published=date_published, url=url)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def add_author_to_article(self, ark_pid, author):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_pid}> schema:author <{author}> .

            }}
        """.format(prefix=self.prefix, ark_pid=ark_pid, author=author)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def delete_author_of_article(self, ark_pid, author):
        sparql_request = """
            {prefix}

            DELETE {{
                <{ark_pid}> schema:author <{author}> .

            }}
            WHERE
            {{
                <{ark_pid}> schema:author <{author}> .
            }}
        """.format(prefix=self.prefix, ark_pid=ark_pid, author=author)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def delete_article(self, ark_pid):
        sparql_request = """
            {prefix}

            DELETE WHERE {{
                <{ark_pid}> ?predicate ?object .

            }}
        """.format(prefix=self.prefix, ark_pid=ark_pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()
