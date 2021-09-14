from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST
from .. import variables


class SparqlPostProjectMethods:
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


    def create_project(self, pid, name, description, founding_date, dissolution_date, url):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{pid}" .

                <{pid}> a schema:ResearchProject ;
                    schema:name \"\"\"{name}\"\"\" ;
                    schema:description \"\"\"{description}\"\"\" ;
                    schema:foundingDate "{founding_date}"^^xsd:date ;
                    schema:dissolutionDate "{dissolution_date}"^^xsd:date ;
                    schema:url \"\"\"{url}\"\"\" ;
                    schema:identifier <{pid}ARK> .
            }}
        """.format(prefix=variables.prefix, pid=pid, name=name, description=description, founding_date=founding_date, dissolution_date=dissolution_date, url=url)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_member_to_project(self, pid, member):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:member <{member}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, member=member)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_member_of_project(self, pid, member):
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:member <{member}> .

            }}
            WHERE
            {{
                <{pid}> schema:member <{member}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, member=member)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_article_to_project(self, pid, article):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:subjectOf <{article}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, article=article)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_article_of_project(self, pid, article):
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:subjectOf <{article}> .

            }}
            WHERE
            {{
                <{pid}> schema:subjectOf <{article}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, article=article)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def add_institution_to_project(self, pid, institution):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}> schema:sponsor <{institution}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, institution=institution)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_project(self, pid):
        sparql_request = """
            {prefix}

            DELETE WHERE {{
                <{pid}> ?predicate ?object .
            }}
        """.format(prefix=variables.prefix, pid=pid)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()


    def delete_institution_from_project(self, pid, institution):
        sparql_request = """
            {prefix}

            DELETE {{
                <{pid}> schema:sponsor <{institution}> .

            }}
            WHERE
            {{
                <{pid}> schema:sponsor <{institution}> .
            }}
        """.format(prefix=variables.prefix, pid=pid, institution=institution)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()
