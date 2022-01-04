import json


def parse_get_sub_organization_institution(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_dict_data = []
    for json_data in loaded_json:
        if len(json_data) > 0:
            dict_data = {
                'sub_organization': json_data['subOrganization']['value'],
            }
            array_dict_data.append(dict_data)
    return array_dict_data


def parse_get_institutions(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_data_parsed = []
    for json_data in loaded_json:
        array_data_parsed.append([json_data['institution']['value'], json_data['name']['value'], json_data['alternateName']['value'] if 'alternateName' in json_data else ''])
    return array_data_parsed


def parse_get_data_institution(sparql_query_answer):
    dict_data = {}
    if len(json.loads(sparql_query_answer)['results']['bindings']) > 0:
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        dict_data = {
            'name': loaded_json['name']['value'],
            'alternate_name': loaded_json['alternateName']['value'] if 'alternateName' in loaded_json else '',
            'description': loaded_json['description']['value'],
            'founding_date': loaded_json['foundingDate']['value'][:10],
            'url': loaded_json['url']['value'],
            'logo': loaded_json['logo']['value'] if 'logo' in loaded_json else '',
        }
    return dict_data
