import json


def parse_get_search(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_data_parsed = []
    for json_data in loaded_json:
        array_data_parsed.append([json_data['project']['value'], json_data['name']['value']])
    return array_data_parsed
