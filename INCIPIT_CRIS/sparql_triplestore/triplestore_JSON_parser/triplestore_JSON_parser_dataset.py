import json


def parse_get_datasets(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_data_parsed = []
    for json_data in loaded_json:
        array_data_parsed.append([json_data['dataset']['value'], json_data['name']['value']])
    return array_data_parsed


def parse_check_dataset_ark(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    if len(loaded_json) > 0:
        return True
    return False


def parse_get_data_dataset(sparql_query_answer):
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
    loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
    dict_data = {
        'url': loaded_json['url']['value'],
    }
    return dict_data
