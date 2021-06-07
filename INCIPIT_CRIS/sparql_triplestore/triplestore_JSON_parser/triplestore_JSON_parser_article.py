import json


def parse_get_articles(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_data_parsed = []
    for json_data in loaded_json:
        array_data_parsed.append([json_data['article']['value'], json_data['name']['value']])
    return array_data_parsed


def parse_check_article_ark(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    if len(loaded_json) > 0:
        return True
    return False


def parse_get_authors_article(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_authors = []
    for author in loaded_json:
        array_authors.append(author['author']['value'])
    return array_authors


def parse_get_data_article(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
    dict_data = {
        'name': loaded_json['name']['value'],
        'abstract': loaded_json['abstract']['value'],
        'datePublished': loaded_json['datePublished']['value'][:10],
    }

    return dict_data