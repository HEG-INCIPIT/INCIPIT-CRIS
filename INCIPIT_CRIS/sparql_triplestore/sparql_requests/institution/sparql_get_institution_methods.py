from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_institution import *
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_generic import *
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

            SELECT ?institution ?name ?alternateName WHERE
            {{
                ?institution a schema:Organization .
                ?institution schema:name ?name .
                ?institution schema:alternateName ?alternateName .
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        array_institutions_parsed = parse_get_institutions(self.sparql.query().response.read())
        array_institutions_parsed.sort(key=lambda item: item[1])

        return array_institutions_parsed


    def get_top_lvl_institutions(self):
        """
        Get basic information of an institution : ark, name,
        And return a list for each institution
        """

        sparql_request = """
            {prefix}

            SELECT ?institution ?name ?parentOrganization WHERE
            {{
                ?institution a schema:Organization .
                ?institution schema:name ?name .
                NOT EXISTS {{
                    ?institution schema:parentOrganization ?parentOrganization
                }}
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        return parse_get_institutions(self.sparql.query().response.read())


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
                <{ark_research}> schema:worksFor ?person .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_persons = []

        result_sparql_request_parser = parse_get_simple_elements(self.sparql.query().response.read(), 'person')

        for worker in result_sparql_request_parser:
            data_person = variables.SparqlGetPersonMethods.get_full_name_person(self, worker)
            array_persons.append(data_person)

        array_persons.sort(key=lambda worker: worker['family_name'])

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
                <{ark_research}> schema:affiliation ?person .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_affiliates = []

        for affiliate in parse_get_simple_elements(self.sparql.query().response.read(), 'person'):
            data_affiliate = variables.SparqlGetPersonMethods.get_full_name_person(self, affiliate)
            array_affiliates.append(data_affiliate)

        array_affiliates.sort(key=lambda worker: worker['family_name'])

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
                ?article a schema:ScholarlyArticle ;
                    schema:sourceOrganization <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        articles = parse_get_simple_elements(self.sparql.query().response.read(), 'article')

        articles_sorted = []
        for article in articles:
            articles_sorted.append(variables.sparql_get_article_object.get_data_article(article))
        articles_sorted.sort(key=lambda item: item['date_published'], reverse=True)

        return articles_sorted


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

        projects = parse_get_simple_elements(self.sparql.query().response.read(), 'project')

        projects_sorted = []
        for project in projects:
            projects_sorted.append(variables.sparql_get_project_object.get_data_project(project))
        projects_sorted.sort(key=lambda item: item['founding_date'], reverse=True)

        return projects_sorted


    def get_datasets_institution(self, pid):
        """
        Get all the datasets of the institution for who the creators were working for
        Return a dictionnary
        """

        sparql_request = """
            {prefix}

            SELECT ?dataset WHERE
            {{
                ?dataset a schema:Dataset ;
                    schema:sourceOrganization <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        datasets = parse_get_simple_elements(self.sparql.query().response.read(), 'dataset')

        datasets_sorted = []
        for dataset in datasets:
            datasets_sorted.append(variables.sparql_get_dataset_object.get_data_dataset(dataset))
        datasets_sorted.sort(key=lambda item: item['modified_date'], reverse=True)

        return datasets_sorted


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
            sub_organization_array.append(variables.SparqlGetInstitutionMethods.get_minimum_data_institution(self, inst))

        parent_organization_array = []
        for inst in variables.SparqlGetInstitutionMethods.get_parent_organization_institution(self, pid):
            parent_organization_array.append(variables.SparqlGetInstitutionMethods.get_minimum_data_institution(self, inst))

        workers = variables.sparql_get_institution_object.get_workers_institution(pid)
        affiliates = variables.sparql_get_institution_object.get_affiliates_institution(pid)

        articles = variables.sparql_get_institution_object.get_articles_institution(pid)
        projects = variables.sparql_get_institution_object.get_projects_institution(pid)
        datasets = variables.sparql_get_institution_object.get_datasets_institution(pid)
        projects_funded = variables.sparql_get_funder_object.get_projects_funder(pid)
        funder = variables.sparql_get_funder_object.check_funder_ark(pid)

        data_institution['workers'] = workers
        data_institution['len_workers'] = len(workers)
        data_institution['affiliates'] = affiliates
        data_institution['len_affiliates'] = len(affiliates)
        data_institution['sub_organizations'] = sub_organization_array
        data_institution['parent_organizations'] = parent_organization_array
        data_institution['articles'] = articles
        data_institution['len_articles'] = len(articles)
        data_institution['projects'] = projects
        data_institution['len_projects'] = len(projects)
        data_institution['datasets'] = datasets
        data_institution['len_datasets'] = len(datasets)
        data_institution['projects_funded'] = projects_funded
        data_institution['len_projects_funded'] = len(projects_funded)
        data_institution['funder'] = funder
        data_institution['pid'] = pid
        return data_institution


    def get_minimum_data_institution(self, pid):
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
        data_institution['pid'] = pid

        return data_institution


    def check_institution_ark(self, pid):
        """
        Return a boolean
        """

        sparql_request = """
            {prefix}

            SELECT ?Organization WHERE
            {{
                <{ark_research}> a ?Organization .
                FILTER(?Organization = schema:Organization)
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)
        return parse_check_ark(self.sparql.query().response.read())
