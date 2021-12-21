import json


def parse_check_ark(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    if len(loaded_json) > 0:
        return True
    return False


def parse_get_simple_elements(sparql_query_answer, name_of_element):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_elements = []
    for element in loaded_json:
        if len(element) > 0:
            array_elements.append(element[name_of_element]['value'])
    return array_elements