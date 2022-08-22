import json


def parse_get_data_article(sparql_query_answer):
    """
    Parse the JSON sparql query answer for the basic information around an article
    """
    dict_data = {
        'name': '',
        'abstract': '',
        'date_published': '',
        'url': '',
    }
    if len(json.loads(sparql_query_answer)['results']['bindings']) > 0:
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        dict_data = {
            'name': loaded_json['name']['value'],
            'abstract': loaded_json['abstract']['value'],
            'date_published': loaded_json['datePublished']['value'][:10],
            'url': loaded_json['url']['value'],
        }

    return dict_data


def parse_get_DOI_information(sparql_query_answer):
    """
    Parse the JSON sparql query answer for getting the DOI of an article
    """
    if len(json.loads(sparql_query_answer)['results']['bindings']) > 0:
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        return loaded_json['value']['value']
    return ''
