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
