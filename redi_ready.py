#! /usr/bin/python3

import sys
import json
from cappy import API, beautify_json
import xml_util
import config
import os

def save_response(project_dir, response):
    prefix = response.cappy_data['call_name'].replace('export_', '').replace('import_', '')
    filename = "{}.{}".format(prefix, response.cappy_data['file_format'])
    path = os.path.join(config.outfile_dir, project_dir, filename)
    print("Writing {} for {}".format(filename, project_dir))
    with open(path, 'w') as outfile:
        outfile.write(str(response.content, 'utf-8'))
    return filename

def write_project_config(api, project_name):
    """
    This function writes all the files we need for our current vagrant spin up process with
    redcap projects
    """
    save_response(project_name, api.export_project_info())
    save_response(project_name, api.export_events())
    save_response(project_name, api.export_arms())
    save_response(project_name, api.export_instruments())
    save_response(project_name, api.export_instrument_event_mapping())
    config.form_events_json = save_response(project_name, api.export_instrument_event_mapping_json())
    save_response(project_name, api.export_metadata())
    save_response(project_name, api.export_records())

def write_form_events(api, project_name):
    """
    This writes most of the form events file from the event map and templates
    """
    print("Writing form events from {}/event_map.json".format(project_name))

    event_map_path = os.path.join(config.outfile_dir, project_name, config.form_events_json)
    with open(event_map_path, 'r') as event_map:
        data = json.loads(event_map.read())

    form_events_path = os.path.join(config.outfile_dir, project_name, 'formEvents.xml')
    with open(form_events_path, 'w') as form_events_file:
        form_events_file.write(xml_util.form_events_render(data))

def write_translation_table(yaml_filename, project_name):
    """
    Writes the translation table xml by using a yaml file and a template
    """
    print("Writing translationTable.xml from data_in/{}".format(yaml_filename))
    yaml_path_in = os.path.join(config.infile_dir, yaml_filename)
    xml_filename = yaml_filename.replace('.yaml', '.xml')
    yaml_path_out = os.path.join(config.outfile_dir, project_name, xml_filename)
    with open(yaml_path_out, 'w') as yaml_file:
        yaml_file.write(xml_util.translation_table_render(yaml_path_in))

def send(api, path, call):
    with open(path, 'r') as in_file:
        data = in_file.read()
        print("=================")
        print("Calling: ", call)
        res = getattr(api, call)(data)
        if res.status_code != 200:
            print("Error: ", res.status_code, " With file at: ", path)
            print("DATA:")
            print(data)
        else:
            print("Success with file at: ", path)
        print("Content: ", res.content)

def main(argv):
    project_name = argv[1]
    index = 2 # the index of the cappy version file redi_ready uses

    if project_name and config.fetch_data:
        pull_api = API(config.source_project['token'],
                  config.source_project['endpoint'],
                  config.versions[index])
        try:
            os.mkdir(os.path.join(config.outfile_dir, project_name))
        except:
            pass

        print("Writing project configs for {}".format(project_name))
        write_project_config(pull_api, project_name)
        write_form_events(pull_api, project_name)
        write_translation_table('translation.yaml', project_name)

    if config.target_project and config.push_data:
        print("Copying redcap info over to {}".format(config.target_project['endpoint']))
        token = config.target_project['super_token']
        endpoint = config.target_project["endpoint"]
        push_api = API(token, endpoint, config.versions[index])
        file_calls = [
            ('project_info.csv', 'create_project'),
            ('arms.csv', 'import_arms'),
            ('events.csv', 'import_events'),
            ('metadata.csv', 'import_metadata'),
            ('instrument_event_mapping.csv', 'import_instrument_event_mapping'),
            ('records.json', 'import_records'),
        ]
        path = os.path.join(config.outfile_dir, project_name)
        path_calls = [(os.path.join(path, item[0]), item[1]) for item in file_calls]
        for item in path_calls:
            filename = item[0]
            call = item[1]
            send(push_api, filename, call)

    print("=========DONE=========")

if __name__ == "__main__":
    main(sys.argv)
