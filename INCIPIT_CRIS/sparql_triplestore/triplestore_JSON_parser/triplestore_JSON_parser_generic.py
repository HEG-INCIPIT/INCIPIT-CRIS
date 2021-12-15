import json


def parse_get_simple_elements_article(sparql_query_answer, name_of_element):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_elements = []
    for element in loaded_json:
        array_elements.append(element[name_of_element]['value'])
    return array_elements