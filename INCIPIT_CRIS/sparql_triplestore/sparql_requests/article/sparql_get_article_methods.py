from SPARQLWrapper import SPARQLWrapper, JSON, GET, DIGEST
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_article import *
from sparql_triplestore.triplestore_JSON_parser.triplestore_JSON_parser_generic import *
from .. import variables


class SparqlGetArticleMethods:
    """
    A class used to do sparql GET requests about a Person to the triplestore

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
    get_articles()
        Gets basic information of an article
    get_authors_article(pid)
        Gets all the authors of an article
    get_projects_article(pid)
        Gets all the projects of an article
    get_datasets_article(pid)
        Gets all the datasets of an article
    get_institutions_article(pid)
        Gets all the institutions of an article
    get_DOI_article(pid)
        Gets the DOI of an article
    get_data_article(pid)
        Gets all the data related to an article
    get_minimum_data_article(pid)
        Gets the minimum data related to an article, it is used to avoid infinite recursiveness between classes
    check_article_ark(pid)
        Check if the ark passed as parameter is attributed to an article
    """


    def __init__(self):

        self.sparql = SPARQLWrapper(variables.url_endpoint)

        self.sparql.setHTTPAuth(DIGEST)
        self.sparql.setCredentials(variables.admin, variables.password)
        self.sparql.setReturnFormat(JSON)
        self.sparql.setMethod(GET)


    def get_articles(self):
        """
        Gets basic information of an article : ark, name

        Returns
        -------
        list
            a list of tuples containing strings that are the ark and the name of the article
        """

        sparql_request = """
            {prefix}

            SELECT ?article ?name WHERE
            {{
                ?article a schema:ScholarlyArticle .
                ?article schema:name ?name .
            }}
        """.format(prefix=variables.prefix)

        self.sparql.setQuery(sparql_request)

        array_article_parsed = parse_get_element_and_name(self.sparql.query().response.read(), 'article')
        array_article_parsed.sort(key=lambda item: item[1])

        return array_article_parsed


    def get_authors_article(self, pid):
        """
        Gets all the authors of an article

        Parameters
        ----------
        pid : str
            persistant identifier of the article

        Returns
        -------
        list
            a list of tuples containing strings that are the ark and a dictionary containing t
            he first name and last name of the author
        """

        sparql_request = """
            {prefix}

            SELECT ?author WHERE
            {{
                <{ark_research}> schema:author ?author .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_authors = []

        for author in parse_get_simple_elements(self.sparql.query().response.read(), 'author'):
            full_name = variables.sparql_get_person_object.get_full_name_person(author)
            array_authors.append([author, full_name])

        # Sort array by alphabetical order taking the family name to do it
        array_authors.sort(key=lambda author: author[1]['family_name'])

        return array_authors


    def get_projects_article(self, pid):
        """
        Gets all the projects of an article

        Parameters
        ----------
        pid : str
            persistant identifier of the article

        Returns
        -------
        dict
            a list containing information about the projects related
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

        for project in parse_get_simple_elements(self.sparql.query().response.read(), 'project'):
            array_projects.append(variables.sparql_get_project_object.get_data_project(project))
        array_projects.sort(key=lambda item: item['founding_date'], reverse=True)
        return array_projects


    def get_datasets_article(self, pid):
        """
        Get all the datasets of an article
        And return an array with tuples (identifier, dictionnary)

        Parameters
        ----------
        pid : str
            persistant identifier of the article

        Returns
        -------
        list
            a list containing information about the datasets related
        """

        sparql_request = """
            {prefix}

            SELECT ?dataset WHERE
            {{
                <{ark_research}> schema:isBasedOn ?dataset .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_datasets = []

        for dataset in parse_get_simple_elements(self.sparql.query().response.read(), 'dataset'):
            array_datasets.append(variables.sparql_get_dataset_object.get_data_dataset(dataset))

        return array_datasets


    def get_institutions_article(self, pid):
        """
        Gets all the institutions of the article for who the authors were working for
        Return a dictionnary

        Parameters
        ----------
        pid : str
            persistant identifier of the article

        Returns
        -------
        list
            a list containing information about the institutions related
        """

        sparql_request = """
            {prefix}

            SELECT ?sourceOrganization WHERE
            {{
                <{ark_research}> schema:sourceOrganization ?sourceOrganization .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        array_institutions = []

        for institution in parse_get_simple_elements(self.sparql.query().response.read(), 'sourceOrganization'):
            data_institution = variables.SparqlGetInstitutionMethods.get_minimum_data_institution(self, institution)
            array_institutions.append(data_institution)

        return array_institutions


    def get_DOI_article(self, pid):
        """
        Gets information about the doi information of the given article

        Parameters
        ----------
        pid : str
            persistant identifier of the article

        Returns
        -------
        str
            a string containing the DOI of the article
        """

        sparql_request = """
            {prefix}

            SELECT ?value WHERE
            {{
                <{pid}DOI> schema:propertyID ?value .
            }}
        """.format(prefix=variables.prefix, pid=pid)

        self.sparql.setQuery(sparql_request)

        return parse_get_DOI_information(self.sparql.query().response.read())


    def get_data_article(self, pid):
        """
        Gets all the information of an article : ark, name, abstract, date of publication, authors, ...
        And return a dictionnary with all elements

        Parameters
        ----------
        pid : str
            persistant identifier of the article
        
        Returns
        -------
        dict
            a dictionary containing all the data related to the article
        """

        sparql_request = """
            {prefix}

            SELECT ?name ?abstract ?datePublished ?url WHERE
            {{
                <{ark_research}> schema:name ?name .
                <{ark_research}> schema:abstract ?abstract .
                <{ark_research}> schema:datePublished ?datePublished .
                <{ark_research}> schema:url ?url .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        data_article = parse_get_data_article(self.sparql.query().response.read())

        authors = variables.sparql_get_article_object.get_authors_article(pid)
        projects = variables.sparql_get_article_object.get_projects_article(pid)
        datasets = variables.sparql_get_article_object.get_datasets_article(pid)
        institutions = variables.sparql_get_article_object.get_institutions_article(pid)
        doi = variables.sparql_get_article_object.get_DOI_article(pid)

        data_article['authors'] = authors
        data_article['len_authors'] = len(authors)
        data_article['projects'] = projects
        data_article['len_projects'] = len(projects)
        data_article['datasets'] = datasets
        data_article['len_datasets'] = len(datasets)
        data_article['institutions'] = institutions
        data_article['doi'] = doi
        data_article['pid'] = pid

        return data_article


    def get_minimum_data_article(self, pid):
        """
        Gets all the information of an article : ark, name, abstract, date of publication, authors, ...
        And return a dictionnary with all elements
        It's a minimum version principaly use to display the main information about an article

        Parameters
        ----------
        pid : str
            persistant identifier of the article

        Returns
        -------
        dict
            a dictionary containing the data related to the article
        """

        sparql_request = """
            {prefix}

            SELECT ?name ?abstract ?datePublished ?url WHERE
            {{
                <{ark_research}> schema:name ?name .
                <{ark_research}> schema:abstract ?abstract .
                <{ark_research}> schema:datePublished ?datePublished .
                <{ark_research}> schema:url ?url .
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)

        data_article = parse_get_data_article(self.sparql.query().response.read())

        authors = variables.sparql_get_article_object.get_authors_article(pid)
        doi = variables.sparql_get_article_object.get_DOI_article(pid)

        data_article['authors'] = authors
        data_article['len_authors'] = len(authors)
        data_article['doi'] = doi
        data_article['pid'] = pid

        return data_article


    def check_article_ark(self, pid):
        """
        Checks if the ark is the ark of an article

        Parameters
        ----------
        pid : str
            persistant identifier of the article

        Returns
        -------
        bool
            a boolean indicating if the ark belongs to an article or not
        """

        sparql_request = """
            {prefix}

            SELECT ?scholarlyArticle WHERE
            {{
                <{ark_research}> a ?scholarlyArticle .
                FILTER(?scholarlyArticle = schema:ScholarlyArticle)
            }}
        """.format(prefix=variables.prefix, ark_research=pid)

        self.sparql.setQuery(sparql_request)
        return parse_check_ark(self.sparql.query().response.read())
