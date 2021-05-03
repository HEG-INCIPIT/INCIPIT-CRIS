import json

class Triplestore_JSON_responses_parser:
    """
    A class used to parse the JSON response of the triplestore

    """
    def parse_get_persons(sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings']
        array_data_parsed = []
        for json_data in loaded_json:
            array_data_parsed.append([json_data['person']['value'], json_data['given_name']['value'], json_data['family_name']['value']])
        return array_data_parsed

    def parse_check_person_ark(sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings']
        if (len(loaded_json) > 0):
            return True
        return False

    def parse_get_data_person(sparql_query_answer):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        print(json.loads(sparql_query_answer))
        dict_data = {
            'given_name': loaded_json['given_name']['value'],
            'family_name': loaded_json['family_name']['value'],
            'email': loaded_json['email']['value'],
            'telephone': loaded_json['telephone']['value'],
            'description': loaded_json['description']['value']
        }
        print(dict_data)
        return dict_data