import json


def parse_get_data_dataset(sparql_query_answer):
    dict_data = {
        'name': '',
        'abstract': '',
        'created_date': '',
        'modified_date': '',
        'url': '',
    }
    if len(json.loads(sparql_query_answer)['results']['bindings']) > 0:
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        dict_data = {
            'name': loaded_json['name']['value'],
            'abstract': loaded_json['abstract']['value'],
            'created_date': loaded_json['dateCreated']['value'][:10],
            'modified_date': loaded_json['dateModified']['value'][:10],
            'url': loaded_json['url']['value'],
        }

    return dict_data


def parse_get_data_download_dataset(sparql_query_answer):
    dict_data = {
            'url': '',
        }

    if len(json.loads(sparql_query_answer)['results']['bindings']) > 0:
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        dict_data = {
            'url': loaded_json['url']['value'],
        }
    return dict_data
