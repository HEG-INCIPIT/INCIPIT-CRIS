from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_project import *
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_generic import *
from .. import variables


class SparqlGetProjectMethods:
    """
    A class used to do sparql GET requests about projects to the triplestore

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


    def get_projects(self):
        """
        Gets basic information of a project : ark, name,
        And return a list for each project
        """

        sparql_request = """
            {prefix}

            SELECT ?project ?name WHERE
            {{
                ?project a schema:ResearchProject .
                ?project schema:name ?name .
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        array_projects_parsed = parse_get_element_and_name(self.sparql.query().response.read(), 'project')
        array_projects_parsed.sort(key=lambda item: item[1])

        return array_projects_parsed


    def get_members_project(self, pid):
        """
        Gets all the members of a project
        And return an array with tuples (identifier, dictionnary)
        """
        from ..person.sparql_get_person_methods import SparqlGetPersonMethods

        sparql_request = """
            {prefix}

            SELECT ?member WHERE
            {{
                <{ark_research}> schema:member ?member .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_members = []

        for member in parse_get_simple_elements(self.sparql.query().response.read(), 'member'):
            full_name = variables.sparql_get_person_object.get_full_name_person(member)
            array_members.append([member, full_name])

        array_members.sort(key=lambda member: member[1]['family_name'])

        return array_members


    def get_articles_project(self, pid):
        """
        Gets all the articles of a project
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?article WHERE
            {{
                <{ark_research}> schema:subjectOf ?article .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        articles = parse_get_simple_elements(self.sparql.query().response.read(), 'article')

        articles_sorted = []
        for article in articles:
            articles_sorted.append(variables.sparql_get_article_object.get_minimum_data_article(article))
        articles_sorted.sort(key=lambda item: item['date_published'], reverse=True)

        return articles_sorted

    def get_datasets_project(self, pid):
        """
        Gets all the datasets of a project
        And return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?dataset WHERE
            {{
                ?dataset schema:producer <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_datasets = []

        for dataset in parse_get_simple_elements(self.sparql.query().response.read(), 'dataset'):
            array_datasets.append(variables.sparql_get_dataset_object.get_data_dataset(dataset))

        return array_datasets


    def get_institutions_project(self, pid):
        """
        Gets all the institutions of the project for who the authors were working for
        Return a dictionnary
        """

        sparql_request = """
            {prefix}

            SELECT ?project WHERE
            {{
                <{ark_research}> schema:sponsor ?project .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_institutions = []

        for institution in parse_get_simple_elements(self.sparql.query().response.read(), 'project'):
            data_institution = variables.SparqlGetInstitutionMethods.get_minimum_data_institution(self, institution)
            array_institutions.append(data_institution)

        return array_institutions


    def get_funders_project(self, pid):
        """
        Gets all the funders of the project for who the authors were working for
        Return a dictionnary
        """

        sparql_request = """
            {prefix}

            SELECT ?project WHERE
            {{
                <{ark_research}> schema:funder ?project .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_funders = []

        for funder in parse_get_simple_elements(self.sparql.query().response.read(), 'project'):
            data_funder = variables.SparqlGetInstitutionMethods.get_minimum_data_institution(self, funder)
            array_funders.append(data_funder)

        return array_funders


    def get_data_project(self, pid):
        """
        Gets all the information of a project : ark, name, abstract, date of publication, members, ...
        And return a dictionnary with all elements
        """
        sparql_request = """
            {prefix}

            SELECT ?name ?description ?foundingDate ?dissolutionDate ?url ?logo WHERE
            {{
                <{ark_research}> schema:name ?name .
                <{ark_research}> schema:description ?description .
                <{ark_research}> schema:foundingDate ?foundingDate .
                <{ark_research}> schema:dissolutionDate ?dissolutionDate .
                <{ark_research}> schema:url ?url .
                OPTIONAL {{ <{ark_research}> schema:logo ?logo }} .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)
        data_project = parse_get_data_project(self.sparql.query().response.read())

        members = variables.sparql_get_project_object.get_members_project(pid)
        articles = variables.sparql_get_project_object.get_articles_project(pid)
        datasets = variables.sparql_get_project_object.get_datasets_project(pid)
        institutions = variables.sparql_get_project_object.get_institutions_project(pid)
        funders = variables.sparql_get_project_object.get_funders_project(pid)

        data_project['members'] = members
        data_project['len_members'] = len(members)
        data_project['articles'] = articles
        data_project['len_articles'] = len(articles)
        data_project['datasets'] = datasets
        data_project['len_datasets'] = len(datasets)
        data_project['institutions'] = institutions
        data_project['len_institutions'] = len(institutions)
        data_project['funders'] = funders
        data_project['len_funders'] = len(funders)
        data_project['pid'] = pid

        return data_project

    def get_minimum_data_project(self, pid):
        """
        Gets all the information of a project : ark, name, abstract, date of publication, members, ...
        And return a dictionnary with all elements
        """
        sparql_request = """
            {prefix}

            SELECT ?name ?description ?foundingDate ?dissolutionDate ?url ?logo WHERE
            {{
                <{ark_research}> schema:name ?name .
                <{ark_research}> schema:description ?description .
                <{ark_research}> schema:foundingDate ?foundingDate .
                <{ark_research}> schema:dissolutionDate ?dissolutionDate .
                <{ark_research}> schema:url ?url .
                OPTIONAL {{ <{ark_research}> schema:logo ?logo }} .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)
        data_project = parse_get_data_project(self.sparql.query().response.read())

        members = variables.sparql_get_project_object.get_members_project(pid)

        data_project['members'] = members
        data_project['len_members'] = len(members)
        data_project['pid'] = pid

        return data_project

    def check_project_ark(self, pid):
        """
        Check if the ark belongs to a project and return a boolean
        """

        sparql_request = """
            {prefix}

            SELECT ?researchProject WHERE
            {{
                <{ark_research}> a ?researchProject .
                FILTER(?researchProject = schema:ResearchProject)
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        return parse_check_ark(self.sparql.query().response.read())
