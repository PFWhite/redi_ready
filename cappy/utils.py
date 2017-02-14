import json
import os
import cappy.cappy_config as config

def beautify_json(json_data, sort=True):
    return json.dumps(json.loads(json_data), indent=4, sort_keys=sort)

def get_version_files():
    version_path = config.versions_path
    files = os.listdir(version_path)
    return [str(f) for f in files if os.path.isfile(os.path.join(version_path, f))]

def path_for_version(filename):
    version_path = config.versions_path
    return os.path.join(version_path, filename)
