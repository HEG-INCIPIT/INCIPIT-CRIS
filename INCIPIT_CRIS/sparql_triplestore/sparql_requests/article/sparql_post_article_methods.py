from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST
from .. import variables


class SparqlPostArticleMethods:
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

    def create_article(self, pid, name, abstract, date_published, url):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{pid}" .

                <{pid}> a schema:ScholarlyArticle ;
                    schema:name \"\"\"{name}\"\"\" ;
                    schema:abstract \"\"\"{abstract}\"\"\" ;
                    schema:datePublished "{date_published}"^^xsd:date ;
                    schema:url \"\"\"{url}\"\"\" ;
                    schema:identifier <{pid}ARK> .

            }}
        """.format(prefix=variables.prefix, pid=pid, name=name, abstract=abstract, date_published=date_published, url=url)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def add_author_to_article(self, pid, author):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:author <{author}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, author=author)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def delete_author_of_article(self, pid, author):
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:author <{author}> .

            }}
            WHERE
            {{
                <{pid}> schema:author <{author}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, author=author)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_project_to_article(self, pid, project):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{project}> schema:subjectOf <{pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, project=project)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_dataset_to_article(self, pid, dataset):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:isBasedOn <{dataset}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, dataset=dataset)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_DOI_article(self, pid, doi_value):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}DOI> a schema:PropertyValue ;
                    schema:name 'DOI' ;
                    schema:propertyID "{doi_value}" .
                
                <{pid}> schema:identifier <{pid}DOI> .
            }}
        """.format(prefix=variables.prefix, pid=pid, doi_value=doi_value)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_DOI_article(self, pid, doi_value):
        sparql_request = """
            {prefix}

            DELETE WHERE {{
                <{pid}DOI> a schema:PropertyValue ;
                    schema:name 'DOI' ;
                    schema:propertyID "{doi_value}" .
                
                <{pid}> schema:identifier <{pid}DOI> .
            }}
        """.format(prefix=variables.prefix, pid=pid, doi_value=doi_value)

        print(sparql_request)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_institution_to_article(self, pid, institution):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:sourceOrganization <{institution}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, institution=institution)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_institution_from_article(self, pid, institution):
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:sourceOrganization <{institution}> .

            }}
            WHERE
            {{
                <{pid}> schema:sourceOrganization <{institution}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, institution=institution)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()
