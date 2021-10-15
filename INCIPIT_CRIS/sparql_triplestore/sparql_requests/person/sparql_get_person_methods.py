from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_person import *
from .. import variables


class SparqlGetPersonMethods:
    """
    A class used to do sparql GET requests about a Person to the triplestore

    Attributes
    ----------
    @url_endpoint : str
        the URL of the triplestore endpoint to do sparql resquests
    @prefix : str
        the prefix of the ontologies used
    @admin : str
        the username of the endpoint used
    @password : str
        the password of the username used for access to the endpoint
    @sparql : SPARQLWrapper
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

    def get_persons(self):
        """
        Get basic information of persons : ark, given name, family name
        And return a list for each person
        """

        sparql_request = """
            {prefix}

            SELECT ?person ?given_name ?family_name WHERE
            {{
                ?person a schema:Person .
                ?person schema:givenName ?given_name .
                ?person schema:familyName ?family_name .
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        return parse_get_persons(self.sparql.query().response.read())

    def get_full_name_person(self, pid):
        """
        Get the full name of a person formated in a dict
        Return a dict with given name and family name
        """
        sparql_request = """
            {prefix}

            SELECT ?given_name ?family_name WHERE
            {{
                <{ark_research}> schema:givenName ?given_name .
                <{ark_research}> schema:familyName ?family_name .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        dict_name = parse_get_full_name_person(self.sparql.query().response.read())
        dict_name['pid'] = pid

        return dict_name

    def get_articles_person(self, pid):
        """
        Get all the articles for who the person is an author
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?article WHERE
            {{
                ?article schema:author <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        articles = parse_get_articles_person(self.sparql.query().response.read())

        articles_sorted = []
        for article in articles:
            articles_sorted.append(variables.sparql_get_article_object.get_data_article(article))    
        articles_sorted.sort(key=lambda item: item['date_published'], reverse=True)

        return articles_sorted


    def get_projects_person(self, pid):
        """
        Get all the projects for who the person is a member
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?project WHERE
            {{
                ?project schema:member <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        projects = parse_get_projects_person(self.sparql.query().response.read())

        projects_sorted = []
        for project in projects:
            projects_sorted.append(variables.sparql_get_project_object.get_data_project(project))    
        projects_sorted.sort(key=lambda item: item['founding_date'], reverse=True)

        return projects_sorted


    def get_datasets_creator_person(self, pid):
        """
        Get all the datasets for who the person is a creator
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?dataset WHERE
            {{
                ?dataset schema:creator <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        datasets = parse_get_datasets_person(self.sparql.query().response.read())

        datasets_sorted = []
        for dataset in datasets:
            datasets_sorted.append(variables.sparql_get_dataset_object.get_data_dataset(dataset))

        return datasets_sorted


    def get_datasets_maintainer_person(self, pid):
        """
        Get all the datasets for who the person is a maintainer
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?dataset WHERE
            {{
                ?dataset schema:maintainer <{ark_research}> .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        datasets = parse_get_datasets_person(self.sparql.query().response.read())

        datasets_sorted = []
        for dataset in datasets:
            datasets_sorted.append(variables.sparql_get_dataset_object.get_data_dataset(dataset))

        return datasets_sorted

    
    def get_work_person(self, pid):
        """
        Get all the works for who the person is a maintainer
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?work WHERE
            {{
                <{ark_research}> schema:worksFor ?work .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_works = []

        for work in parse_get_works_person(self.sparql.query().response.read()):
            data_work = variables.SparqlGetInstitutionMethods.get_data_institution(self, work)
            array_works.append(data_work)

        return array_works


    def get_affiliation_person(self, pid):
        """
        Get all the affiliations for who the person is a maintainer
        Return an array with tuples (identifier, dictionnary)
        """

        sparql_request = """
            {prefix}

            SELECT ?affiliation WHERE
            {{
                <{ark_research}> schema:affiliation ?affiliation .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_affiliations = []

        for affiliation in parse_get_affiliations_person(self.sparql.query().response.read()):
            data_affiliation = variables.SparqlGetInstitutionMethods.get_data_institution(self, affiliation)
            array_affiliations.append(data_affiliation)

        return array_affiliations

    
    def get_job_title_person(self, pid):
        """
        Get information about the job title of the given person
        """

        sparql_request = """
            {prefix}

            SELECT ?jobTitle WHERE
            {{
                <{pid}> schema:jobTitle ?jobTitle .
            }}
        """.format(prefix=variables.prefix, pid=pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_job_title(self.sparql.query().response.read())


    def get_title_person(self, pid):
        """
        Get information about the job title of the given person
        """

        sparql_request = """
            {prefix}

            SELECT ?honorificPrefix WHERE
            {{
                <{pid}> schema:honorificPrefix ?honorificPrefix .
            }}
        """.format(prefix=variables.prefix, pid=pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_title(self.sparql.query().response.read())


    def get_IN_information_person(self, pid):
        """
        Get information about the LinkedIn information of the given person
        """

        sparql_request = """
            {prefix}

            SELECT ?url WHERE
            {{
                <{pid}IN> schema:url ?url .
            }}
        """.format(prefix=variables.prefix, pid=pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_IN_information(self.sparql.query().response.read())


    def get_data_person(self, pid):
        """
        Get all the information of a person : ark, given name, family name, ...
        Return a dictionnary with all elements
        """

        sparql_request = """
            {prefix}

            SELECT ?given_name ?family_name ?email ?telephone ?description ?address WHERE
            {{
                <{ark_research}> schema:givenName ?given_name .
                <{ark_research}> schema:familyName ?family_name .
                OPTIONAL {{ <{ark_research}> schema:email ?email }}
                OPTIONAL {{ <{ark_research}> schema:telephone ?telephone }}
                OPTIONAL {{ <{ark_research}> schema:description ?description }}
                OPTIONAL {{ <{ark_research}> schema:address ?address }}

            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        data_person = parse_get_data_person(self.sparql.query().response.read())

        articles = variables.sparql_get_person_object.get_articles_person(pid)
        projects = variables.sparql_get_person_object.get_projects_person(pid)
        datasets_creator = variables.sparql_get_person_object.get_datasets_creator_person(pid)
        datasets_maintainer = variables.sparql_get_person_object.get_datasets_maintainer_person(pid)
        works = variables.sparql_get_person_object.get_work_person(pid)
        affiliations = variables.sparql_get_person_object.get_affiliation_person(pid)
        job_title = variables.sparql_get_person_object.get_job_title_person(pid)
        title = variables.sparql_get_person_object.get_title_person(pid)

        # Concatenate the two arrays of datasets in only one with only one recurrency
        datasets = datasets_maintainer
        datasets_maintainer_pid = [ dataset['pid'] for dataset in datasets_maintainer ]
        for dataset in datasets_creator:
            if not (dataset['pid'] in datasets_maintainer_pid):
                datasets.append(dataset)
        datasets.sort(key=lambda item: item['modified_date'], reverse=True)

        
        data_person['pid'] = pid
        data_person['articles'] = articles
        data_person['len_articles'] = len(articles)
        data_person['projects'] = projects
        data_person['len_projects'] = len(projects)
        data_person['datasets'] = datasets
        data_person['len_datasets'] = len(datasets)
        data_person['works'] = works
        data_person['affiliations'] = affiliations
        data_person['job_title'] = job_title
        data_person['title'] = title

        return data_person

    def check_person_ark(self, pid):
        """
        Return a boolean
        """

        sparql_request = """
            {prefix}

            SELECT ?person WHERE
            {{
                <{ark_research}> a ?person .
                FILTER(?person = schema:Person)
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)
        return parse_check_person_ark(self.sparql.query().response.read())
