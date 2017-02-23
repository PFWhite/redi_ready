#! /usr/bin/python

import sys
import json
from cappy import API, beautify_json
import xml_util
import config
import os

def save_response(project_dir, filename, content, filetype):
    path = os.path.join(config.outfile_dir, project_dir, filename)
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
    yaml_path_in = os.path.join(config.infile_dir, yaml_filename)
    xml_filename = yaml_filename.replace('.yaml', '.xml')
    yaml_path_out = os.path.join(config.outfile_dir, project_name, xml_filename)
    with open(yaml_path_out, 'w') as yaml_file:
        yaml_file.write(xml_util.translation_table_render(yaml_path_in))


def main(argv):
    filetype = argv[2]
    index = 1 if filetype == 'json' else 0
    api = API(config.token, config.endpoint, config.versions[index])
    project_name = argv[1]
    if project_name:
        try:
            os.mkdir(os.path.join(config.outfile_dir, project_name))
        except:
            pass

        write_project_config(api, project_name, filetype)
        write_form_events(api, project_name)
        # write_translation_table('translation.yaml', project_name)

if __name__ == "__main__":
    main(sys.argv)
