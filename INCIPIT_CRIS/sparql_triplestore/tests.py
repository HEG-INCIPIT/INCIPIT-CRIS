from django.test import TestCase
from .triplestore_JSON_parser.triplestore_JSON_parser_generic import *
from .triplestore_JSON_parser.triplestore_JSON_parser_article import *
from .triplestore_JSON_parser.triplestore_JSON_parser_dataset import *
from .triplestore_JSON_parser.triplestore_JSON_parser_institution import *

# Create your tests here.

class GenericJSONParser(TestCase):
    
    def setUp(self):
        # parse_get_simple_elements
        self.get_authors_article = b'{ "head": {\n    "vars": [ "author" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "author": { "type": "uri" , "value": "ark:/99999/1" }\n      } ,\n \
            { \n        "author": { "type": "uri" , "value": "ark:/99999/2" }\n      } ,\n \
            { \n        "author": { "type": "uri" , "value": "ark:/99999/3" }\n      }\n    ]\n  }\n}\n'

        self.get_authors_article_empty = b'{ "head": {\n    "vars": [ "author" ]\n  } ,\n  "results": {\n    "bindings": [\n { \n } \n \n]\n  }\n}\n'

        self.get_projects_article = b'{ "head": {\n    "vars": [ "project" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "project": { "type": "uri" , "value": "ark:/99999/1" }\n      } ,\n \
            { \n        "project": { "type": "uri" , "value": "ark:/99999/2" }\n      } ,\n \
            { \n        "project": { "type": "uri" , "value": "ark:/99999/3" }\n      }\n    ]\n  }\n}\n'

        self.get_projects_article_empty = b'{ "head": {\n    "vars": [ "project" ]\n  } ,\n  "results": {\n    "bindings": [\n { \n } \n]\n  }\n}\n'

        # Data of sub organizations
        self.sub_organization_institution = b'{ "head": {\n    "vars": [ "subOrganization" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "subOrganization": { "type": "uri" , "value": "ark:/99999/1" }\n      } ,\n \
            { \n        "subOrganization": { "type": "uri" , "value": "ark:/99999/2" }\n      } ,\n \
            { \n        "subOrganization": { "type": "uri" , "value": "ark:/99999/3" }\n      }\n    ]\n  }\n}\n'

        self.sub_organization_institution_empty = b'{ "head": {\n    "vars": [ "subOrganization" ]\n  } ,\n  "results": {\n    "bindings": [\n { \n } \n]\n  }\n}\n'

        # Data of parent organizations
        self.parent_organization_institution = b'{ "head": {\n    "vars": [ "parentOrganization" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "parentOrganization": { "type": "uri" , "value": "ark:/99999/1" }\n      } ,\n \
            { \n        "parentOrganization": { "type": "uri" , "value": "ark:/99999/2" }\n      } ,\n \
            { \n        "parentOrganization": { "type": "uri" , "value": "ark:/99999/3" }\n      }\n    ]\n  }\n}\n'

        self.parent_organization_institution_empty = b'{ "head": {\n    "vars": [ "parentOrganization" ]\n  } ,\n  "results": {\n    "bindings": [\n { \n } \n]\n  }\n}\n'

        # parse_check_article_ark

        self.check_article_true = b'{ "head": {\n    "vars": [ "scholarlyArticle" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "scholarlyArticle": { "type": "uri" , "value": "https://schema.org/ScholarlyArticle" }\n      }\n    ]\n  }\n}\n'

        self.check_article_false = b'{ "head": {\n    "vars": [ "scholarlyArticle" ]\n  } ,\n  "results": {\n    "bindings": [\n    \n]\n  }\n}\n'


    def tests_JSON_parser(self):
        # parse_get_simple_elements
        self.assertEqual(parse_get_simple_elements(self.get_authors_article, 'author'), ['ark:/99999/1', 'ark:/99999/2', 'ark:/99999/3'])
        self.assertEqual(parse_get_simple_elements(self.get_authors_article_empty, 'author'), [])

        self.assertEqual(parse_get_simple_elements(self.get_projects_article, 'project'), ['ark:/99999/1', 'ark:/99999/2', 'ark:/99999/3'])
        self.assertEqual(parse_get_simple_elements(self.get_projects_article_empty, 'project'), [])

        self.assertEqual(parse_get_simple_elements(self.sub_organization_institution, 'subOrganization'), ['ark:/99999/1', 'ark:/99999/2', 'ark:/99999/3'])
        self.assertEqual(parse_get_simple_elements(self.sub_organization_institution_empty, 'subOrganization'), [])
        self.assertEqual(parse_get_simple_elements(self.parent_organization_institution, 'parentOrganization'), ['ark:/99999/1', 'ark:/99999/2', 'ark:/99999/3'])
        self.assertEqual(parse_get_simple_elements(self.parent_organization_institution_empty, 'parentOrganization'), [])

        # parse_check_ark
        self.assertEqual(parse_check_ark(self.check_article_true), True)
        self.assertEqual(parse_check_ark(self.check_article_false), False)


class ArticleJSONParser(TestCase):

    def setUp(self):
        # parse_get_articles
        self.get_articles = b'{ "head": {\n    "vars": [ "article" , "name" ]\n  } ,\n "results": { \n    "bindings": [\n \
            { \n        "article": { "type": "uri" , "value": "ark:/99999/test1" } ,\n \
            "name": { "type": "literal" , "value": "Name test 1" }\n      } ,\n \
            { \n        "article": { "type": "uri" , "value": "ark:/99999/test2" } ,\n \
            "name": { "type": "literal" , "value": "Name test 2" }\n      }\n    ]\n  }\n}\n'
        
        self.get_articles_empty = b'{ "head": {\n    "vars": [ "article" , "name" ]\n  } ,\n "results": { \n    "bindings": [\n \n]\n  }\n}\n'

        # parse_get_data_article
        self.get_data_article = b'{ "head": {\n    "vars": [ "name" , "abstract" , "datePublished" , "url" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "name": { "type": "literal" , "value": "Article name test" } ,\
            \n        "abstract": { "type": "literal" , "value": "Article abstract test" } ,\
            \n        "datePublished": { "type": "literal" , "datatype": "http://www.w3.org/2001/XMLSchema#date" , "value": "2022-01-01 00:00:00+00:00" } ,\
            \n        "url": { "type": "literal" , "value": "www.url.ch" }\n      }\n    ]\n  }\n}\n'

        self.get_data_article_empty = b'{ "head": {\n    "vars": ["name" , "abstract" , "datePublished" , "url"]\n  } ,\n  "results": {\n    "bindings": [\n \n ]\n }\n}\n'

        # parse_get_DOI_information
        self.get_DOI_information = b'{ "head": {\n    "vars": [ "value" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "value": { "type": "literal" , "value": "10.1" }\n      }\n    ]\n  }\n}\n'
        
        self.get_DOI_information_empty = b'{ "head": {\n    "vars": [ "value" ]\n  } ,\n  "results": {\n    "bindings": [\n \n]\n  }\n}\n'


    def tests_JSON_parser(self):
        # parse_get_articles
        self.assertEqual(parse_get_articles(self.get_articles), [['ark:/99999/test1', 'Name test 1'], ['ark:/99999/test2', 'Name test 2']] )
        self.assertEqual(parse_get_articles(self.get_articles_empty), [] )

        # parse_get_data_article
        self.assertEqual(parse_get_data_article(self.get_data_article), {'name': 'Article name test', 'abstract': 'Article abstract test', 'date_published': '2022-01-01', 'url': 'www.url.ch'})
        self.assertEqual(parse_get_data_article(self.get_data_article_empty), {'name': '', 'abstract': '', 'date_published': '', 'url': ''})

        # parse_get_DOI_information
        self.assertEqual(parse_get_DOI_information(self.get_DOI_information), '10.1')
        self.assertEqual(parse_get_DOI_information(self.get_DOI_information_empty), '')


class DatasetJSONParser(TestCase):
    
    def setUp(self):
        # parse_get_datasets
        self.get_datasets = b'{ "head": {\n    "vars": [ "dataset" , "name" ]\n  } ,\n "results": { \n    "bindings": [\n \
            { \n        "dataset": { "type": "uri" , "value": "ark:/99999/test1" } ,\n \
            "name": { "type": "literal" , "value": "Name test 1" }\n      } ,\n \
            { \n        "dataset": { "type": "uri" , "value": "ark:/99999/test2" } ,\n \
            "name": { "type": "literal" , "value": "Name test 2" }\n      }\n    ]\n  }\n}\n'
        
        self.get_datasets_empty = b'{ "head": {\n    "vars": [ "dataset" , "name" ]\n  } ,\n "results": { \n    "bindings": [\n   \n]\n  }\n}\n'

        # parse_get_data_dataset
        self.get_data_dataset = b'{ "head": {\n    "vars": [ "name" , "abstract" , "dateCreated", "dateModified" , "url" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "name": { "type": "literal" , "value": "Dataset name test" } ,\
            \n        "abstract": { "type": "literal" , "value": "Dataset abstract test" } ,\
            \n        "dateCreated": { "type": "literal" , "datatype": "http://www.w3.org/2001/XMLSchema#date" , "value": "2021-01-01 00:00:00+00:00" } ,\
            \n        "dateModified": { "type": "literal" , "datatype": "http://www.w3.org/2001/XMLSchema#date" , "value": "2022-01-01 00:00:00+00:00" } ,\
            \n        "url": { "type": "literal" , "value": "www.url.ch" }\n      }\n    ]\n  }\n}\n'

        self.get_data_dataset_empty = b'{ "head": {\n    "vars": ["name" , "abstract" , "datePublished" , "url"]\n  } ,\n  "results": {\n    "bindings": [\n \n ]\n }\n}\n'

        # parse_get_data_download_dataset
        self.get_data_download_dataset = b'{ "head": {\n    "vars": [ "url" ]\n  } ,\n "results": { \n    "bindings": [\n \
            { \n        "url": { "type": "literal" , "value": "www.url.ch" }\n      }\n    ]\n  }\n}\n'
        
        self.get_data_download_dataset_empty = b'{ "head": {\n    "vars": [ "url" ]\n  } ,\n "results": { \n    "bindings": [\n \n]\n  }\n}\n'

    def tests_JSON_parser(self):
        # parse_get_simple_elements_dataset
        self.assertEqual(parse_get_datasets(self.get_datasets), [['ark:/99999/test1', 'Name test 1'], ['ark:/99999/test2', 'Name test 2']])
        self.assertEqual(parse_get_datasets(self.get_datasets_empty), [])

        # parse_get_data_dataset
        self.assertEqual(parse_get_data_dataset(self.get_data_dataset), {'name': 'Dataset name test', 'abstract': 'Dataset abstract test', 'created_date': '2021-01-01', 'modified_date': '2022-01-01', 'url': 'www.url.ch'})
        self.assertEqual(parse_get_data_dataset(self.get_data_dataset_empty), {'name': '', 'abstract': '', 'created_date': '', 'modified_date': '', 'url': ''})

        # parse_get_data_download_dataset
        self.assertEqual(parse_get_data_download_dataset(self.get_data_download_dataset), {'url': 'www.url.ch'})
        self.assertEqual(parse_get_data_download_dataset(self.get_data_download_dataset_empty), {'url': ''})


class InstitutionJSONParser(TestCase):
    
    def setUp(self):

        # Data of sub organizations
        self.sub_organization_institution = b'{ "head": {\n    "vars": [ "subOrganization" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "subOrganization": { "type": "uri" , "value": "ark:/99999/1" }\n      } ,\n \
            { \n        "subOrganization": { "type": "uri" , "value": "ark:/99999/2" }\n      } ,\n \
            { \n        "subOrganization": { "type": "uri" , "value": "ark:/99999/3" }\n      }\n    ]\n  }\n}\n'

        self.sub_organization_institution_empty = b'{ "head": {\n    "vars": [ "subOrganization" ]\n  } ,\n  "results": {\n    "bindings": [\n \n]\n  }\n}\n'

        # Data of parent organizations
        self.parent_organization_institution = b'{ "head": {\n    "vars": [ "parentOrganization" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "parentOrganization": { "type": "uri" , "value": "ark:/99999/1" }\n      } ,\n \
            { \n        "parentOrganization": { "type": "uri" , "value": "ark:/99999/2" }\n      } ,\n \
            { \n        "parentOrganization": { "type": "uri" , "value": "ark:/99999/3" }\n      }\n    ]\n  }\n}\n'

        self.parent_organization_institution_empty = b'{ "head": {\n    "vars": [ "parentOrganization" ]\n  } ,\n  "results": {\n    "bindings": [\n \n]\n  }\n}\n'

        # parse_get_institutions
        self.get_institutions = b'{ "head": {\n    "vars": [ "institution" , "name" , "alternateName" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "institution": { "type": "uri" , "value": "ark:/99999/1" } ,\n        "name": { "type": "literal" , "value": "First institution" } ,\n        "alternateName": { "type": "literal" , "value": "Fi" }\n      } ,\n      \
            { \n        "institution": { "type": "uri" , "value": "ark:/99999/2" } ,\n        "name": { "type": "literal" , "value": "Second institution" } ,\n        "alternateName": { "type": "literal" , "value": "" }\n      } ,\n      \
            { \n        "institution": { "type": "uri" , "value": "ark:/99999/3" } ,\n        "name": { "type": "literal" , "value": "Third institution" } ,\n        "alternateName": { "type": "literal" , "value": "T i" }\n      }\n    ]\n  }\n}\n'
        
        self.get_institutions_empty = b'{ "head": {\n    "vars": [ "institution" , "name" , "alternateName" ]\n  } ,\n  "results": {\n    "bindings": [\n \n ]\n  }\n}\n'

        # parse_get_data_institution
        self.get_data_institution = b'{ "head": {\n    "vars": [ "name" , "alternateName" , "description" , "foundingDate" , "url" , "logo" , "parentOrganization" , "subOrganization" ]\n  } ,\n  "results": {\n    "bindings": [\n      { \n\
            "name": { "type": "literal" , "value": "My institution" } ,\n        \
            "alternateName": { "type": "literal" , "value": "M i" } ,\n        \
            "description": { "type": "literal" , "value": "This is a test description" } ,\n        \
            "foundingDate": { "type": "literal" , "datatype": "http://www.w3.org/2001/XMLSchema#date" , "value": "None" } ,\n        \
            "url": { "type": "literal" , "value": "" } ,\n        \
            "logo": { "type": "literal" , "value": "logo.png" }\n      \
            }\n    ]\n  }\n}\n'

        self.get_data_institution_empty = b'{ "head": {\n    "vars": [ "name" , "alternateName" , "description" , "foundingDate" , "url" , "logo" , "parentOrganization" , "subOrganization" ]\n  } ,\n  "results": {\n    "bindings": [\n    \n]\n  }\n}\n'


    def tests_JSON_parser(self):
        # parse_get_sub_organization_institution
        self.assertEqual(parse_get_sub_organization_institution(self.sub_organization_institution), [{'sub_organization': 'ark:/99999/1'}, {'sub_organization': 'ark:/99999/2'}, {'sub_organization': 'ark:/99999/3'}])
        self.assertEqual(parse_get_sub_organization_institution(self.sub_organization_institution_empty), [])

        # parse_get_institutions
        self.assertEqual(parse_get_institutions(self.get_institutions), [['ark:/99999/1', 'First institution', 'Fi'], ['ark:/99999/2', 'Second institution', ''], ['ark:/99999/3', 'Third institution', 'T i']])
        self.assertEqual(parse_get_institutions(self.get_institutions_empty), [])

        # parse_get_data_institution
        self.assertEqual(parse_get_data_institution(self.get_data_institution), {'name': 'My institution', 'alternate_name': 'M i', 'description': 'This is a test description', 'founding_date': 'None', 'url': '', 'logo': 'logo.png'})
        self.assertEqual(parse_get_data_institution(self.get_data_institution_empty), {})


class PersonJSONParser(TestCase):
    
    def setUp(self):

        # Data of sub organizations
        self.get_persons = b'{ "head": {\n    "vars": [ "person" , "given_name" , "family_name" , "jobTitle" ]\n  } ,\n  "results": {\n    "bindings": [\n      { \n        \
            "person": { "type": "uri" , "value": "ark:/99999/1" } ,\n        \
            "given_name": { "type": "literal" , "value": "Test" } ,\n        \
            "family_name": { "type": "literal" , "value": "Name" } ,\n        \
            "jobTitle": { "type": "literal" , "value": "Job Title" }\n      \
            } ,\n      { \n        \
            "person": { "type": "uri" , "value": "ark:/99999/2" } ,\n        \
            "given_name": { "type": "literal" , "value": "Another" } ,\n        \
            "family_name": { "type": "literal" , "value": "Test" }\n      } ,\
            }\n    ]\n  }\n}\n'

    def tests_JSON_parser(self):
        # parse_get_persons
        self.assertEqual(self.get_persons(self.get_persons), [{'person': 'ark:/99999/1', 'given_name': 'Test', 'family_name': 'Name', 'job_title': 'Job Title'}, {'person': 'ark:/99999/1', 'given_name': 'Test', 'family_name': 'Name'}])
