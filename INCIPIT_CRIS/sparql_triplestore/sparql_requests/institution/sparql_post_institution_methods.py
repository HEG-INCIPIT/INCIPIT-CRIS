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

    def create_institution(self, pid, name, alternateName, description, founding_date, url):
        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{pid}ARK> a schema:PropertyValue ;
                    schema:propertyID 'ARK' ;
                    schema:value "{pid}" .

                <{pid}> a schema:ResearchOrganization ;
                    schema:name \"\"\"{name}\"\"\" ;
                    schema:alternateName \"\"\"{alternateName}\"\"\" ;
                    schema:description \"\"\"{description}\"\"\" ;
                    schema:foundingDate ""{founding_date}"^^xsd:date ;
                    schema:url \"\"\"{url}\"\"\" ;
                    schema:identifier <{pid}ARK> .

            }}
        """.format(prefix=variables.prefix, pid=pid, name=name, alternateName=alternateName, description=description, founding_date=founding_date, url=url)

        self.sparql.setQuery(sparql_request)

        return self.sparql.query().response.read()