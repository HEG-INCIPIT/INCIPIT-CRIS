from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST
from .. import variables


class SparqlPostInstitutionMethods:
    """
    A class used to do sparql POST requests about an Institution to the triplestore

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


    def create_institution(self, pid, name, alternate_name, description, founding_date, url, logo, upper_organisation):
        """
        Create an institution ressource
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{pid}" .

                <{pid}> a schema:Organization ;
                    schema:name \"\"\"{name}\"\"\" ;
                    schema:alternateName \"\"\"{alternate_name}\"\"\" ;
                    schema:description \"\"\"{description}\"\"\" ;
                    schema:foundingDate "{founding_date}"^^xsd:date ;
                    schema:url \"\"\"{url}\"\"\" ;
                    schema:logo \"\"\"{logo}\"\"\" ;
                    {has_upper_organisation}
                    schema:identifier <{pid}ARK> .

            }}
        """.format(prefix=variables.prefix, pid=pid, name=name, alternate_name=alternate_name, description=description, 
        founding_date=founding_date, url=url, logo=logo, has_upper_organisation='' if upper_organisation == '' else 'schema:parentOrganization <{}> ;'.format(upper_organisation))

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_parent_institution_to_institution(self, pid, institution):
        """
        Adds a parent institution to the given institution using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:parentOrganization <{institution}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, institution=institution)

        self.sparql.setQuery(sparql_request)
        
        return self.sparql.query().response.read()


    def delete_parent_institution_to_institution(self, pid, institution):
        """
        Deletes a parent institution from the given institution using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:parentOrganization <{institution}> .

            }}
            WHERE
            {{
                <{pid}> schema:parentOrganization <{institution}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, institution=institution)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_sub_institution_to_institution(self, pid, institution):
        """
        Adds a child institution to the given institution using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{institution}> schema:parentOrganization <{pid}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, institution=institution)

        self.sparql.setQuery(sparql_request)
        
        return self.sparql.query().response.read()


    def delete_sub_institution_to_institution(self, pid, institution):
        """
        Deletes a child institution to the given institution using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            DELETE {{
                <{institution}> schema:parentOrganization <{pid}> .

            }}
            WHERE
            {{
                <{institution}> schema:parentOrganization <{pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, institution=institution)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_worker_to_institution(self, pid, worker):
        """
        Adds a worker to the given institution using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:worksFor <{worker}> .
            }}
        """.format(prefix=variables.prefix, pid=pid , worker=worker)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_affiliate_to_institution(self, pid, affiliate):
        """
        Adds an affiliate to the given institution using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:affiliation <{affiliate}> .
            }}
        """.format(prefix=variables.prefix, pid=pid , affiliate=affiliate)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_article_to_institution(self, pid, article):
        """
        Adds an article to the given institution using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{article}> schema:sourceOrganization <{pid}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, article=article)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_project_to_institution(self, pid, project):
        """
        Adds a project to the given institution using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{project}> schema:sponsor <{pid}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, project=project)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_dataset_to_institution(self, pid, dataset):
        """
        Adds a dataset to the given institution using pid's for both ressources
        """
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{dataset}> schema:sourceOrganization <{pid}> .

            }}
        """.format(prefix=variables.prefix, pid=pid, dataset=dataset)

        self.sparql.setQuery(sparql_request)
        
        return self.sparql.query().response.read()
