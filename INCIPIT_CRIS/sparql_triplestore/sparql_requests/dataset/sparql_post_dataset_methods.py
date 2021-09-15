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


    def create_dataset(self, pid, name, abstract, date_created, date_modified, url_data, url_details):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{pid}" .

                <{pid}DD> a schema:DataDownload ;
                    schema:url "{url_data}" .

                <{pid}> a schema:Dataset ;
                    schema:name \"\"\"{name}\"\"\" ;
                    schema:abstract \"\"\"{abstract}\"\"\" ;
                    schema:dateCreated "{date_created}"^^xsd:date ;
                    schema:dateModified "{date_modified}"^^xsd:date ;
                    schema:url \"\"\"{url_details}\"\"\" ;
                    schema:identifier <{pid}ARK> ;
                    schema:distribution <{pid}DD> .

            }}
        """.format(prefix=variables.prefix, pid=pid, name=name, abstract=abstract, 
            date_created=date_created, date_modified=date_modified, url_data=url_data, url_details=url_details)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_maintainer_to_dataset(self, pid, maintainer):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:maintainer <{maintainer}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, maintainer=maintainer)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_maintainer_of_dataset(self, pid, maintainer):
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:maintainer <{maintainer}> .

            }}
            WHERE
            {{
                <{pid}> schema:maintainer <{maintainer}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, maintainer=maintainer)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_creator_to_dataset(self, pid, creator):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:creator <{creator}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, creator=creator)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_creator_of_dataset(self, pid, creator):
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:creator <{creator}> .

            }}
            WHERE
            {{
                <{pid}> schema:creator <{creator}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, creator=creator)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_project_to_dataset(self, pid, project):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:producer <{project}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, project=project)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_project_from_dataset(self, pid, project):
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:producer <{project}> .

            }}
            WHERE
            {{
                <{pid}> schema:producer <{project}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, project=project)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()

    def add_article_to_dataset(self, pid, article):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{article}> schema:isBasedOn <{pid}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, article=article)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_article_from_dataset(self, pid, article):
        sparql_request = """
            {prefix}

            DELETE {{
                <{article}> schema:isBasedOn <{pid}> .

            }}
            WHERE
            {{
                <{article}> schema:isBasedOn <{pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, article=article)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_institution_to_dataset(self, pid, institution):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:sourceOrganization <{institution}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, institution=institution)

        self.sparql.setQuery(sparql_request)
        
        return self.sparql.query().response.read()


    def delete_institution_from_dataset(self, pid, institution):
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
