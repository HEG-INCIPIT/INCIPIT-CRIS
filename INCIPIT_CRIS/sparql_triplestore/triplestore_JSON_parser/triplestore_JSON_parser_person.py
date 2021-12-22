import json


def parse_get_persons(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_data_parsed = []
    for json_data in loaded_json:
        array_data_parsed.append(
            [json_data['person']['value'], json_data['given_name']['value'], json_data['family_name']['value'], json_data['jobTitle']['value'] if 'jobTitle' in json_data else ''])
    return array_data_parsed


def parse_get_full_name_person(sparql_query_answer):
    dict_data = {}
    if len(json.loads(sparql_query_answer)['results']['bindings']) > 0:
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        dict_data = {
            'given_name': loaded_json['given_name']['value'],
            'family_name': loaded_json['family_name']['value'],
        }
    return dict_data


def parse_get_job_title(sparql_query_answer):
    if len(json.loads(sparql_query_answer)['results']['bindings']) > 0:
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        return loaded_json['jobTitle']['value']
    return ''


def parse_get_ORCID_information(sparql_query_answer):
    if len(json.loads(sparql_query_answer)['results']['bindings']) > 0:
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        return loaded_json['propertyID']['value']
    return ''


def parse_get_IN_information(sparql_query_answer):
    if len(json.loads(sparql_query_answer)['results']['bindings']) > 0:
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        return loaded_json['url']['value']
    return ''


def parse_get_data_person(sparql_query_answer):
    print(sparql_query_answer)
    loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
    dict_data = {
        'given_name': loaded_json['given_name']['value'],
        'family_name': loaded_json['family_name']['value'],
    }

    # If email has a value in triplestore, the value is inserted in dict, if not empty string is inserted
    if loaded_json.get('email') is not None:
        dict_data['email'] = loaded_json['email']['value']
    else:
        dict_data['email'] = ''

    # If telephone has a value in triplestore, the value is inserted in dict, if not empty string is inserted
    if loaded_json.get('telephone') is not None:
        dict_data['telephone'] = loaded_json['telephone']['value']
    else:
        dict_data['telephone'] = ''

    # If description has a value in triplestore, the value is inserted in dict, if not empty string is inserted
    if loaded_json.get('description') is not None:
        dict_data['description'] = loaded_json['description']['value']
    else:
        dict_data['description'] = ''

    # If address has a value in triplestore, the value is inserted in dict, if not empty string is inserted
    if loaded_json.get('address') is not None:
        dict_data['address'] = loaded_json['address']['value']
    else:
        dict_data['address'] = ''

    return dict_data
