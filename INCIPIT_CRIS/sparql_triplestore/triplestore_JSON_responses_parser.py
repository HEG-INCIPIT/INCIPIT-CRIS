import json


class TriplestoreJSONResponsesParser:
    """
    A class used to parse the JSON response of the triplestore

    """

    ##################################################
    # Person
    ##################################################

    def parse_get_persons(self, sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings']
        array_data_parsed = []
        for json_data in loaded_json:
            array_data_parsed.append(
                [json_data['person']['value'], json_data['given_name']['value'], json_data['family_name']['value']])
        return array_data_parsed

    def parse_get_full_name_person(self, sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        dict_data = {
            'given_name': loaded_json['given_name']['value'],
            'family_name': loaded_json['family_name']['value'],
        }
        return dict_data

    def parse_get_articles_person(self, sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings']
        array_articles = []
        for article in loaded_json:
            array_articles.append(article['article']['value'])
        return array_articles

    def parse_check_person_ark(self, sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings']
        if (len(loaded_json) > 0):
            return True
        return False

    def parse_get_data_person(self, sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        dict_data = {
            'given_name': loaded_json['given_name']['value'],
            'family_name': loaded_json['family_name']['value'],
        }

        # If email has a value in triplestore, the value is inserted in dict, if not empty string is inserted
        if (loaded_json.get('email') != None):
            dict_data['email'] = loaded_json['email']['value']
        else:
            dict_data['email'] = ''

        # If telephone has a value in triplestore, the value is inserted in dict, if not empty string is inserted
        if (loaded_json.get('telephone') != None):
            dict_data['telephone'] = loaded_json['telephone']['value']
        else:
            dict_data['telephone'] = ''

        # If description has a value in triplestore, the value is inserted in dict, if not empty string is inserted
        if (loaded_json.get('description') != None):
            dict_data['description'] = loaded_json['description']['value']
        else:
            dict_data['description'] = ''

        return dict_data

    ##################################################
    # Article
    ##################################################

    def parse_get_articles(self, sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings']
        array_data_parsed = []
        for json_data in loaded_json:
            array_data_parsed.append([json_data['article']['value'], json_data['name']['value']])
        return array_data_parsed

    def parse_check_article_ark(self, sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings']
        if (len(loaded_json) > 0):
            return True
        return False

    def parse_get_authors_article(self, sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings']
        array_authors = []
        for author in loaded_json:
            array_authors.append(author['author']['value'])
        return array_authors

    def parse_get_data_article(self, sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        dict_data = {
            'name': loaded_json['name']['value'],
            'abstract': loaded_json['abstract']['value'],
            'datePublished': loaded_json['datePublished']['value'][:10],
        }

        return dict_data
