from SPARQLWrapper import SPARQLWrapper, JSON, POST, DIGEST

class Sparql_post_methods:
    url_endpoint = 'http://localhost:3030/INCIPIT-CRIS/'
    prefix = """
        PREFIX vivo: <http://vivoweb.org/ontology/core#>
        PREFIX foaf: <http://xmlns.com/foaf/>
        PREFIX vcard: <https://www.w3.org/2006/vcard/ns#>
        PREFIX ark: <http://ark.ch/>
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

        print(family_name)

        sparql_request = """
            {prefix}

            INSERT DATA {{
                <{ark_id}> a foaf:Person ;
                    vcard:hasGivenName '{given_name}' ;
                    vcard:hasFamilyName '{family_name}' ;
                    vcard:email '' ;
                    vcard:hasTelephone '' ;
                    vivo:overview '' .

            }}
        """.format(prefix=self.prefix, ark_id=ark_id, given_name=given_name, family_name=family_name)

        self.sparql.setQuery(sparql_request)

        print(self.sparql.query().response.read())

if __name__ == "__main__":
    sparql = Sparql_post_methods()
    print(sparql.init_person("ark/0000", "David", "nogueiras"))
