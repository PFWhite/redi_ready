#! /usr/bin/python3

import sys
import json
from cappy import API, beautify_json
import xml_util
import config
import os

def save_response(project_dir, filename, content, filetype):
    path = os.path.join(config.outfile_dir, project_dir, filename)
    print("Writing {} for {}".format(filename, project_dir))
    with open(path, 'w') as outfile:
        if filetype == 'json':
            outfile.write(beautify_json(content))
        else:
            outfile.write(str(content, 'utf-8'))

def write_project_config(api, project_name, filetype):
    """
    This function writes all the files we need for our current vagrant spin up process with
    redcap projects
    """
    project_dir = project_name
    save_response(project_dir, 'event.{}'.format(filetype), api.export_events().content, filetype)
    save_response(project_dir, 'arm.{}'.format(filetype), api.export_arms().content, filetype)
    save_response(project_dir, 'instruments.{}'.format(filetype), api.export_instruments().content, filetype)
    save_response(project_dir, 'event_map.{}'.format(filetype), api.export_instrument_event_mapping().content, filetype)
    save_response(project_dir, 'metadata.{}'.format(filetype), api.export_metadata().content, filetype)
    save_response(project_dir, 'records.{}'.format(filetype), api.export_records().content, filetype)
    save_response(project_dir, 'project.info', api.export_project_info().content, filetype)

    # path = os.path.join(config.outfile_dir, project_dir, 'admin_user.token')
    # with open(path, 'w') as file:
    #     file.write(config.token)

    with open(config.get_settings_ini_path(project_dir), 'w') as file:
        file.write(config.settings_ini_string.format(filetype))

    with open(config.get_project_config_path(project_dir), 'w') as file:
        file.write(config.project_config_string.format(project_name, 0, 1))

def write_form_events(api, project_name):
    """
    This writes most of the form events file from the event map and templates
    """
    print("Writing form events from {}/event_map.json".format(project_name))

    event_map_path = os.path.join(config.outfile_dir, project_name, 'event_map.json')
    with open(event_map_path, 'r') as event_map:
        data = json.loads(event_map.read())

    form_events_path = os.path.join(config.outfile_dir, project_name, 'formEvents.xml')
    with open(form_events_path, 'w') as form_events_file:
        form_events_file.write(xml_util.form_events_render(data))

def write_translation_table(yaml_filename, project_name):
    """
    Writes the translation table xml by using a yaml file and a template
    """
    print("Writing translationTable.xml from data_in/{}".formay(yaml_filename))
    yaml_path_in = os.path.join(config.infile_dir, yaml_filename)
    xml_filename = yaml_filename.replace('.yaml', '.xml')
    yaml_path_out = os.path.join(config.outfile_dir, project_name, xml_filename)
    with open(yaml_path_out, 'w') as yaml_file:
        yaml_file.write(xml_util.translation_table_render(yaml_path_in))

def send_call(api, path, call):
    with open(path, 'r') as in_file:
        data = in_file.read()
        print("=================")
        print("Calling: ", call)
        res = getattr(api, call)(data)
        if res.status_code != 200:
            print("Error: ", res.status_code, " With file at: ", path)
        else:
            print("Success with file at: ", path)
        print("Content: ", res.content)

def main(argv):
    project_name = argv[1]
    filetype = argv[2]
    index = {
        'json': 1,
        'csv': 0,
        'xml': 2,
    }[filetype]

    if project_name and config.fetch_data:
        api = API(config.token, config.endpoint, config.versions[index])
        try:
            os.mkdir(os.path.join(config.outfile_dir, project_name))
        except:
            pass

        print("Writing project configs for {}".format(project_name))
        write_project_config(api, project_name, filetype)
        write_form_events(api, project_name)
        # write_translation_table('translation.yaml', project_name)

    if config.target_project and config.push_data:
        print("Copying redcap info over to {}".format(config.target_project['endpoint']))
        token = config.target_project['token']
        endpoint = config.target_project["endpoint"]
        send_api = API(token, endpoint, config.versions[index])
        file_calls = [
            ('arm.{}'.format(filetype), 'import_arms'),
            ('event.{}'.format(filetype), 'import_events'),
            ('metadata.{}'.format(filetype), 'import_metadata'),
            ('event_map.{}'.format(filetype), 'import_instrument_event_mapping'),
            ('records.{}'.format(filetype), 'import_records'),
        ]
        path = os.path.join(config.outfile_dir, project_name)
        path_calls = [(os.path.join(path, item[0]), item[1]) for item in file_calls]
        for item in path_calls:
            filename = item[0]
            call = item[1]
            send_call(send_api, filename, call)

    print("=========DONE=========")

if __name__ == "__main__":
    main(sys.argv)
