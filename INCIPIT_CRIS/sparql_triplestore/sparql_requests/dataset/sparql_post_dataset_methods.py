from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST
from .. import variables


class SparqlPostDatasetMethods:
    """
    A class used to do sparql POST requests about a dataset to the triplestore

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


    def create_dataset(self, ark_pid, name, abstract, date_created, date_modified, url):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{ark_pid}" .

                <{ark_pid}> a schema:Dataset ;
                    schema:name \"\"\"{name}\"\"\" ;
                    schema:abstract \"\"\"{abstract}\"\"\" ;
                    schema:dateCreated "{date_created}"^^xsd:date ;
                    schema:dateModified "{date_modified}"^^xsd:date ;
                    schema:url \"\"\"{url}\"\"\" ;
                    schema:identifier <{ark_pid}ARK> .

            }}
        """.format(prefix=variables.prefix, ark_pid=ark_pid, name=name, abstract=abstract, date_created=date_created, date_modified=date_modified, url=url)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_maintainer_to_dataset(self, ark_pid, maintainer):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_pid}> schema:maintainer <{maintainer}> .

            }}
        """.format(prefix=variables.prefix, ark_pid=ark_pid, maintainer=maintainer)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_maintainer_of_dataset(self, ark_pid, maintainer):
        sparql_request = """
            {prefix}

            DELETE {{
                <{ark_pid}> schema:maintainer <{maintainer}> .

            }}
            WHERE
            {{
                <{ark_pid}> schema:maintainer <{maintainer}> .
            }}
        """.format(prefix=variables.prefix, ark_pid=ark_pid, maintainer=maintainer)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()