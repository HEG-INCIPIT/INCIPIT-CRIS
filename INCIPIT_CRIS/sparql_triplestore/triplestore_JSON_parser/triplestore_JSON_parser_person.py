import json


def parse_get_persons(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_data_parsed = []
    for json_data in loaded_json:
        array_data_parsed.append(
            [json_data['person']['value'], json_data['given_name']['value'], json_data['family_name']['value']])
    return array_data_parsed


def parse_get_full_name_person(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
    dict_data = {
        'given_name': loaded_json['given_name']['value'],
        'family_name': loaded_json['family_name']['value'],
    }
    return dict_data


def parse_get_articles_person(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_articles = []
    for article in loaded_json:
        array_articles.append(article['article']['value'])
    return array_articles


def parse_check_person_ark(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    if len(loaded_json) > 0:
        return True
    return False


def parse_get_data_person(sparql_query_answer):
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

    return dict_data