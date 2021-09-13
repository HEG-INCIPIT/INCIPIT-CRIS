import json


def parse_get_full_name_institution(sparql_query_answer):
    if len(json.loads(sparql_query_answer)['results']['bindings']) > 0:
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        dict_data = {
            'name': loaded_json['name']['value'],
            'alternate_name': loaded_json['alternateNamed']['value'] if 'alternateNamed' in loaded_json else '',
        }
    else:
        dict_data = {
            'name': '',
            'alternate_name': '',
        }
    return dict_data


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


def parse_get_array_sub_organization_institution(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_dict_data = []
    for json_data in loaded_json:
        if len(json_data) > 0:
            array_dict_data.append(json_data['subOrganization']['value'])
    return array_dict_data


def parse_get_array_parent_organization_institution(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_dict_data = []
    for json_data in loaded_json:
        if len(json_data) > 0:
            array_dict_data.append(json_data['parentOrganization']['value'])
    return array_dict_data


def parse_get_institutions(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_data_parsed = []
    for json_data in loaded_json:
        array_data_parsed.append([json_data['institution']['value'], json_data['name']['value']])
    return array_data_parsed


def parse_check_institution_ark(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    if len(loaded_json) > 0:
        return True
    return False


def parse_get_data_institution(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
    dict_data = {
        'name': loaded_json['name']['value'],
        'alternate_name': loaded_json['alternateName']['value'],
        'description': loaded_json['description']['value'],
        'founding_date': loaded_json['foundingDate']['value'][:10],
        'url': loaded_json['url']['value'],
        'logo': loaded_json['logo']['value'] if 'logo' in loaded_json else '',
        'parent_organization': loaded_json['parentOrganization']['value'] if 'parentOrganization' in loaded_json else '',
        'sub_organization': loaded_json['subOrganization']['value'] if 'subOrganization' in loaded_json else '',
    }

    return dict_data


def parse_get_persons_institution(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_persons = []
    for person in loaded_json:
        array_persons.append(person['person']['value'])
        
    return array_persons


def parse_get_articles_institution(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_articles = []
    for article in loaded_json:
        array_articles.append(article['article']['value'])
        
    return array_articles


def parse_get_projects_institution(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_projects = []
    for project in loaded_json:
        array_projects.append(project['sponsor']['value'])
        
    return array_projects


def parse_get_datasets_institution(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_datasets = []
    for dataset in loaded_json:
        array_datasets.append(dataset['dataset']['value'])
        
    return array_datasets
