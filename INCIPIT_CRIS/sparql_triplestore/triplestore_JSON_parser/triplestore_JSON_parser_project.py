import json


def parse_get_projects(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_data_parsed = []
    for json_data in loaded_json:
        array_data_parsed.append([json_data['project']['value'], json_data['name']['value']])
    return array_data_parsed


def parse_get_full_name_project(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
    dict_data = {
        'name': loaded_json['name']['value'],
    }
    return dict_data


def parse_check_project_ark(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    if len(loaded_json) > 0:
        return True
    return False


def parse_get_members_project(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_members = []
    for member in loaded_json:
        array_members.append(member['member']['value'])
    return array_members


def parse_get_articles_project(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings']
    array_articles = []
    for article in loaded_json:
        array_articles.append(article['article']['value'])
    return array_articles


def parse_get_data_project(sparql_query_answer):
    loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
    dict_data = {
        'name': loaded_json['name']['value'],
        'description': loaded_json['description']['value'],
        'founding_date': loaded_json['foundingDate']['value'][:10],
        'dissolution_date': loaded_json['dissolutionDate']['value'][:10],
        'url': loaded_json['url']['value'],
    }

    return dict_data
