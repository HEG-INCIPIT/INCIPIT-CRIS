from django.test import TestCase
from .triplestore_JSON_parser.triplestore_JSON_parser_generic import *
from .triplestore_JSON_parser.triplestore_JSON_parser_article import *
from .triplestore_JSON_parser.triplestore_JSON_parser_dataset import *

# Create your tests here.

class GenericJSONParser(TestCase):
    
    def setUp(self):
        # parse_get_simple_elements_article
        self.get_authors_article = b'{ "head": {\n    "vars": [ "author" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "author": { "type": "uri" , "value": "ark:/99999/1" }\n      } ,\n \
            { \n        "author": { "type": "uri" , "value": "ark:/99999/2" }\n      } ,\n \
            { \n        "author": { "type": "uri" , "value": "ark:/99999/3" }\n      }\n    ]\n  }\n}\n'

        self.get_authors_article_empty = b'{ "head": {\n    "vars": [ "author" ]\n  } ,\n  "results": {\n    "bindings": [\n \n]\n  }\n}\n'

        self.get_projects_article = b'{ "head": {\n    "vars": [ "project" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "project": { "type": "uri" , "value": "ark:/99999/1" }\n      } ,\n \
            { \n        "project": { "type": "uri" , "value": "ark:/99999/2" }\n      } ,\n \
            { \n        "project": { "type": "uri" , "value": "ark:/99999/3" }\n      }\n    ]\n  }\n}\n'

        self.get_projects_article_empty = b'{ "head": {\n    "vars": [ "project" ]\n  } ,\n  "results": {\n    "bindings": [\n \n]\n  }\n}\n'

        # parse_check_article_ark

        self.check_article_true = b'{ "head": {\n    "vars": [ "scholarlyArticle" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "scholarlyArticle": { "type": "uri" , "value": "https://schema.org/ScholarlyArticle" }\n      }\n    ]\n  }\n}\n'

        self.check_article_false = b'{ "head": {\n    "vars": [ "scholarlyArticle" ]\n  } ,\n  "results": {\n    "bindings": [\n    \n]\n  }\n}\n'


    def tests_JSON_parser(self):
        # parse_get_simple_elements_article
        self.assertEqual(parse_get_simple_elements_article(self.get_authors_article, 'author'), ['ark:/99999/1', 'ark:/99999/2', 'ark:/99999/3'])
        self.assertEqual(parse_get_simple_elements_article(self.get_authors_article_empty, 'author'), [])

        self.assertEqual(parse_get_simple_elements_article(self.get_projects_article, 'project'), ['ark:/99999/1', 'ark:/99999/2', 'ark:/99999/3'])
        self.assertEqual(parse_get_simple_elements_article(self.get_projects_article_empty, 'project'), [])

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
        
        self.get_articles_empty = b'{ "head": {\n    "vars": [ "article" , "name" ]\n  } ,\n "results": { \n    "bindings": [\n     \n]\n  }\n}\n'

        # parse_get_data_article
        self.get_data_article = b'{ "head": {\n    "vars": [ "name" , "abstract" , "datePublished" , "url" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "name": { "type": "literal" , "value": "Article name test" } ,\
            \n        "abstract": { "type": "literal" , "value": "Article abstract test" } ,\
            \n        "datePublished": { "type": "literal" , "datatype": "http://www.w3.org/2001/XMLSchema#date" , "value": "2022-01-01 00:00:00+00:00" } ,\
            \n        "url": { "type": "literal" , "value": "www.url.ch" }\n      }\n    ]\n  }\n}\n'

        self.get_data_article_empty = b'{ "head": {\n    "vars": ["name" , "abstract" , "datePublished" , "url"]\n  } ,\n  "results": {\n    "bindings": [\n ]\n }\n}\n'

        # parse_get_DOI_information
        self.get_DOI_information = b'{ "head": {\n    "vars": [ "value" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "value": { "type": "literal" , "value": "10.1" }\n      }\n    ]\n  }\n}\n'
        
        self.get_DOI_information_empty = b'{ "head": {\n    "vars": [ "value" ]\n  } ,\n  "results": {\n    "bindings": [\n    \n]\n  }\n}\n'


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
        
        self.get_datasets_empty = b'{ "head": {\n    "vars": [ "dataset" , "name" ]\n  } ,\n "results": { \n    "bindings": [\n     \n]\n  }\n}\n'

        # parse_get_data_dataset
        self.get_data_dataset = b'{ "head": {\n    "vars": [ "name" , "abstract" , "dateCreated", "dateModified" , "url" ]\n  } ,\n  "results": {\n    "bindings": [\n \
            { \n        "name": { "type": "literal" , "value": "Dataset name test" } ,\
            \n        "abstract": { "type": "literal" , "value": "Dataset abstract test" } ,\
            \n        "dateCreated": { "type": "literal" , "datatype": "http://www.w3.org/2001/XMLSchema#date" , "value": "2021-01-01 00:00:00+00:00" } ,\
            \n        "dateModified": { "type": "literal" , "datatype": "http://www.w3.org/2001/XMLSchema#date" , "value": "2022-01-01 00:00:00+00:00" } ,\
            \n        "url": { "type": "literal" , "value": "www.url.ch" }\n      }\n    ]\n  }\n}\n'

        self.get_data_dataset_empty = b'{ "head": {\n    "vars": ["name" , "abstract" , "datePublished" , "url"]\n  } ,\n  "results": {\n    "bindings": [\n ]\n }\n}\n'

        # parse_get_data_download_dataset
        self.get_data_download_dataset = b'{ "head": {\n    "vars": [ "url" ]\n  } ,\n "results": { \n    "bindings": [\n \
            { \n        "url": { "type": "literal" , "value": "www.url.ch" }\n      }\n    ]\n  }\n}\n'
        
        self.get_data_download_dataset_empty = b'{ "head": {\n    "vars": [ "url" ]\n  } ,\n "results": { \n    "bindings": [\n     \n]\n  }\n}\n'

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