from django.test import TestCase
from .triplestore_JSON_parser.triplestore_JSON_parser_article import *

# Create your tests here.
class ArticleJSONParser(TestCase):
    #######################################################################################################################################
    # Creating json variables to test parser
    #######################################################################################################################################
    
    # parse_get_articles

    get_articles = b'{ "head": {\n    "vars": [ "article" , "name" ]\n  } ,\n "results": { \n    "bindings": [\n \
        { \n        "article": { "type": "uri" , "value": "ark:/99999/test1" } ,\n \
        "name": { "type": "literal" , "value": "Name test 1" }\n      } ,\n \
        { \n        "article": { "type": "uri" , "value": "ark:/99999/test2" } ,\n \
        "name": { "type": "literal" , "value": "Name test 2" }\n      }\n    ]\n  }\n}\n'
    
    get_articles_empty = b'{ "head": {\n    "vars": [ "article" , "name" ]\n  } ,\n "results": { \n    "bindings": [\n     \n]\n  }\n}\n'

    # parse_check_article_ark

    check_article_true = b'{ "head": {\n    "vars": [ "scholarlyArticle" ]\n  } ,\n  "results": {\n    "bindings": [\n \
        { \n        "scholarlyArticle": { "type": "uri" , "value": "https://schema.org/ScholarlyArticle" }\n      }\n    ]\n  }\n}\n'

    check_article_false = b'{ "head": {\n    "vars": [ "scholarlyArticle" ]\n  } ,\n  "results": {\n    "bindings": [\n    \n]\n  }\n}\n'

    # parse_get_simple_elements_article

    get_authors_article = b'{ "head": {\n    "vars": [ "author" ]\n  } ,\n  "results": {\n    "bindings": [\n \
        { \n        "author": { "type": "uri" , "value": "ark:/99999/1" }\n      } ,\n \
        { \n        "author": { "type": "uri" , "value": "ark:/99999/2" }\n      } ,\n \
        { \n        "author": { "type": "uri" , "value": "ark:/99999/3" }\n      }\n    ]\n  }\n}\n'

    get_authors_article_empty = b'{ "head": {\n    "vars": [ "author" ]\n  } ,\n  "results": {\n    "bindings": [\n \n]\n  }\n}\n'

    get_projects_article = b'{ "head": {\n    "vars": [ "project" ]\n  } ,\n  "results": {\n    "bindings": [\n \
        { \n        "project": { "type": "uri" , "value": "ark:/99999/1" }\n      } ,\n \
        { \n        "project": { "type": "uri" , "value": "ark:/99999/2" }\n      } ,\n \
        { \n        "project": { "type": "uri" , "value": "ark:/99999/3" }\n      }\n    ]\n  }\n}\n'

    get_projects_article_empty = b'{ "head": {\n    "vars": [ "project" ]\n  } ,\n  "results": {\n    "bindings": [\n \n]\n  }\n}\n'

    # parse_get_data_article
    get_data_article = b'{ "head": {\n    "vars": [ "name" , "abstract" , "datePublished" , "url" ]\n  } ,\n  "results": {\n    "bindings": [\n \
        { \n        "name": { "type": "literal" , "value": "Article name test" } ,\
        \n        "abstract": { "type": "literal" , "value": "Article abstract test" } ,\
        \n        "datePublished": { "type": "literal" , "datatype": "http://www.w3.org/2001/XMLSchema#date" , "value": "2022-01-01 00:00:00+00:00" } ,\
        \n        "url": { "type": "literal" , "value": "www.url.ch" }\n      }\n    ]\n  }\n}\n'

    get_data_article_empty = b'{ "head": {\n    "vars": ["name" , "abstract" , "datePublished" , "url"]\n  } ,\n  "results": {\n    "bindings": [\n ]\n }\n}\n'

    # parse_get_DOI_information
    get_DOI_information = b'{ "head": {\n    "vars": [ "value" ]\n  } ,\n  "results": {\n    "bindings": [\n \
        { \n        "value": { "type": "literal" , "value": "10.1" }\n      }\n    ]\n  }\n}\n'
    
    get_DOI_information_empty = b'{ "head": {\n    "vars": [ "value" ]\n  } ,\n  "results": {\n    "bindings": [\n    \n]\n  }\n}\n'


    def test_article_JSON_parser(self):
        # parse_get_articles
        self.assertEqual(parse_get_articles(self.get_articles), [['ark:/99999/test1', 'Name test 1'], ['ark:/99999/test2', 'Name test 2']] )
        self.assertEqual(parse_get_articles(self.get_articles_empty), [] )

        # parse_check_article_ark
        self.assertEqual(parse_check_article_ark(self.check_article_true), True)
        self.assertEqual(parse_check_article_ark(self.check_article_false), False)

        # parse_get_simple_elements_article
        self.assertEqual(parse_get_simple_elements_article(self.get_authors_article, 'author'), ['ark:/99999/1', 'ark:/99999/2', 'ark:/99999/3'])
        self.assertEqual(parse_get_simple_elements_article(self.get_authors_article_empty, 'author'), [])

        self.assertEqual(parse_get_simple_elements_article(self.get_projects_article, 'project'), ['ark:/99999/1', 'ark:/99999/2', 'ark:/99999/3'])
        self.assertEqual(parse_get_simple_elements_article(self.get_projects_article_empty, 'project'), [])

        # parse_get_data_article
        self.assertEqual(parse_get_data_article(self.get_data_article), {'name': 'Article name test', 'abstract': 'Article abstract test', 'date_published': '2022-01-01', 'url': 'www.url.ch'})
        self.assertEqual(parse_get_data_article(self.get_data_article_empty), {'name': '', 'abstract': '', 'date_published': '', 'url': ''})

        # parse_get_DOI_information
        self.assertEqual(parse_get_DOI_information(self.get_DOI_information), '10.1')
        self.assertEqual(parse_get_DOI_information(self.get_DOI_information_empty), '')