import json


def parse_get_data_project(sparql_query_answer):
    if(len(json.loads(sparql_query_answer)['results']['bindings']) > 0):
        loaded_json = json.loads(sparql_query_answer)['results']['bindings'][0]
        dict_data = {
            'name': loaded_json['name']['value'],
            'description': loaded_json['description']['value'],
            'founding_date': loaded_json['foundingDate']['value'][:10],
            'dissolution_date': loaded_json['dissolutionDate']['value'][:10],
            'url': loaded_json['url']['value'],
            'logo': loaded_json['logo']['value'] if 'logo' in loaded_json else '',
        }

        return dict_data
    
    return {}
