import json

def beautify_json(json_data, sort=True):
    return json.dumps(json.loads(json_data), indent=4, sort_keys=sort)
