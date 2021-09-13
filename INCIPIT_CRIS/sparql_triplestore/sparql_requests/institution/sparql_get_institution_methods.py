from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_institution import *
from .. import variables


class SparqlGetInstitutionMethods:
    """
    A class used to do sparql GET requests about institutions to the triplestore

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
        self.sparql.setMethod(GET)


    def get_institutions(self):
        """
        Get basic information of an institution : ark, name,
        And return a list for each institution
        """

        sparql_request = """
            {prefix}

            SELECT ?institution ?name ?parentOrganization WHERE
            {{
                ?institution a schema:CollegeOrUniversity .
                ?institution schema:name ?name .
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        return parse_get_institutions(self.sparql.query().response.read())

    
    def get_top_lvl_institutions(self):
        """
        Get basic information of an institution : ark, name,
        And return a list for each institution
        """

        sparql_request = """
            {prefix}

            SELECT ?institution ?name ?parentOrganization WHERE
            {{
                ?institution a schema:CollegeOrUniversity .
                ?institution schema:name ?name .
                NOT EXISTS {{
                    ?institution schema:parentOrganization ?parentOrganization
                }}
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        return parse_get_institutions(self.sparql.query().response.read())


    def get_full_name_institution(self, pid):
        """
        Get the name of an institution formated in a dict
        Return a dict with name
        """
        sparql_request = """
            {prefix}

            SELECT ?name WHERE
            {{
                <{ark_research}> schema:name ?name .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_full_name_institution(self.sparql.query().response.read())


    def get_projects_institution(self, pid):
        """
        Get all the projects of an institution
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?project WHERE
            {{
                ?project schema:subjectOf <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_projects = []

        for project in parse_get_projects_institution(self.sparql.query().response.read()):
            name = variables.sparql_get_project_object.get_full_name_project(project)
            array_projects.append([project, name])

        return array_projects

    
    def get_sub_organization_institution(self, pid):

        sparql_request = """
            {prefix}

            SELECT ?subOrganization WHERE
            {{
                OPTIONAL {{ ?subOrganization schema:parentOrganization <{ark_research}> }} .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_array_sub_organization_institution(self.sparql.query().response.read())

    
    def get_parent_organization_institution(self, pid):

        sparql_request = """
            {prefix}

            SELECT ?parentOrganization WHERE
            {{
                OPTIONAL {{ <{ark_research}> schema:parentOrganization ?parentOrganization }} .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_array_parent_organization_institution(self.sparql.query().response.read())


    def get_dict_institution(self, pid):
        
        sparql_request = """
            {prefix}

            SELECT ?subOrganization WHERE
            {{
                OPTIONAL {{ ?subOrganization schema:parentOrganization <{ark_research}> }} .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_sub_organizations = parse_get_sub_organization_institution(self.sparql.query().response.read())

        institution_dict = {}
        cnt = 0

        data_institution = variables.sparql_get_institution_object.get_data_institution(pid)

        for sub_organization in array_sub_organizations:
            if len(sub_organization) > 0:
                institution_dict['sub_organization{}'.format(cnt)] = variables.sparql_get_institution_object.get_dict_institution(sub_organization['sub_organization'])
            
            cnt+=1

        institution_dict['organization'] = data_institution
        
        return institution_dict


    def get_workers_institution(self, pid):
        """
        Get all the works for who the person is a maintainer
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?person WHERE
            {{
                ?person schema:worksFor <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_persons = []

        for worker in parse_get_persons_institution(self.sparql.query().response.read()):
            print("\n")
            print(worker)
            print("\n")
            data_person = variables.SparqlGetPersonMethods.get_full_name_person(self, worker)
            array_persons.append(data_person)

        return array_persons

    
    def get_affiliates_institution(self, pid):
        """
        Get all the affiliations for who the person is a maintainer
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?person WHERE
            {{
                ?person schema:affiliation <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_affiliates = []

        for affiliate in parse_get_persons_institution(self.sparql.query().response.read()):
            data_affiliate = variables.SparqlGetPersonMethods.get_full_name_person(self, affiliate)
            array_affiliates.append(data_affiliate)

        return array_affiliates


    def get_articles_institution(self, pid):
        """
        Get all the articles of the institution for who the authors were working for
        Return a dictionnary
        """

        sparql_request = """
            {prefix}

            SELECT ?article WHERE
            {{
                ?article schema:sourceOrganisation <{ark_research}> .
                FILTER (?article a schema:ScholarlyArticle)
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_articles = []

        for article in parse_get_articles_institution(self.sparql.query().response.read()):
            data_article = variables.SparqlGetArticleMethods.get_full_name_article(self, article)
            array_articles.append(data_article)

        return array_articles


    def get_projects_institution(self, pid):
        """
        Get all the projects of the institution for who the creators were working for
        Return a dictionnary
        """

        sparql_request = """
            {prefix}

            SELECT ?project WHERE
            {{
                ?project schema:sponsor <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_projects = []

        for project in parse_get_projects_institution(self.sparql.query().response.read()):
            data_project = variables.SparqlGetProjectMethods.get_full_name_project(self, project)
            array_projects.append(data_project)

        return array_projects


    def get_datasets_institution(self, pid):
        """
        Get all the datasets of the institution for who the creators were working for
        Return a dictionnary
        """

        sparql_request = """
            {prefix}

            SELECT ?dataset WHERE
            {{
                ?dataset schema:sourceOrganisation <{ark_research}> .
                FILTER (?dataset a schema:ResearchProject)
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_datasets = []

        for dataset in parse_get_datasets_institution(self.sparql.query().response.read()):
            data_dataset = variables.SparqlGetDatasetMethods.get_full_name_dataset(self, dataset)
            array_datasets.append(data_dataset)

        return array_datasets


    def get_data_institution(self, pid):
        """
        Get all the information of an institution : ark, name, abstract, date of publication, authors, ...
        And return a dictionnary with all elements
        """

        sparql_request = """
            {prefix}

            SELECT ?name ?alternateName ?description ?foundingDate ?url ?logo ?parentOrganization ?subOrganization WHERE
            {{
                <{ark_research}> schema:name ?name .
                OPTIONAL {{ <{ark_research}> schema:alternateName ?alternateName }} .
                OPTIONAL {{ <{ark_research}> schema:description ?description }} .
                <{ark_research}> schema:foundingDate ?foundingDate .
                OPTIONAL {{ <{ark_research}> schema:url ?url }} .
                OPTIONAL {{ <{ark_research}> schema:logo ?logo }} .
                OPTIONAL {{ <{ark_research}> schema:parentOrganization ?parentOrganization }} .
                OPTIONAL {{ ?subOrganization schema:parentOrganization <{ark_research}> }} .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        data_institution = parse_get_data_institution(self.sparql.query().response.read())

        sub_organization_array = []
        for inst in variables.SparqlGetInstitutionMethods.get_sub_organization_institution(self, pid):
            sub_organization_array.append((inst, variables.SparqlGetInstitutionMethods.get_full_name_institution(self, inst)))

        parent_organization_array = []
        for inst in variables.SparqlGetInstitutionMethods.get_parent_organization_institution(self, pid):
            parent_organization_array.append((inst, variables.SparqlGetInstitutionMethods.get_full_name_institution(self, inst)))

        projects = variables.sparql_get_institution_object.get_projects_institution(pid)
        workers = variables.sparql_get_institution_object.get_workers_institution(pid)
        affiliates = variables.sparql_get_institution_object.get_affiliates_institution(pid)
        
        data_institution['projects'] = projects
        data_institution['workers'] = workers
        data_institution['affiliates'] = affiliates
        data_institution['sub_organizations'] = sub_organization_array
        data_institution['parent_organizations'] = parent_organization_array
        data_institution['pid'] = pid
        return data_institution


    def check_institution_ark(self, pid):
        """
        Return a boolean
        """

        sparql_request = """
            {prefix}

            SELECT ?collegeOrUniversity WHERE
            {{
                <{ark_research}> a ?collegeOrUniversity .
                FILTER(?collegeOrUniversity = schema:CollegeOrUniversity)
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)
        return parse_check_institution_ark(self.sparql.query().response.read())
