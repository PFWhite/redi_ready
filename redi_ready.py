#! /usr/bin/python

import sys
import json
from cappy import API, beautify_json
import xml_util
import config
import os

def save_response(project_dir, filename, content):
    path = os.path.join(config.outfile_dir, project_dir, filename)
    with open(path, 'w') as outfile:
        outfile.write(beautify_json(content, False))

def write_project_config(api, project_name):
    project_dir = project_name
    save_response(project_dir, 'event.json', api.export_events().content)
    save_response(project_dir, 'instruments.json', api.export_instruments().content)
    save_response(project_dir, 'event_map.json', api.export_instrument_event_mapping().content)
    save_response(project_dir, 'metadata.json', api.export_metadata().content)
    save_response(project_dir, 'project.info', api.export_project_info().content)

    path = os.path.join(config.outfile_dir, project_dir, 'admin_user.token')
    with open(path, 'w') as file:
        file.write(config.token)

    path = os.path.join(config.outfile_dir, project_dir, 'settings.ini')
    with open(path, 'w') as file:
        file.write('IMPORT_CONTENT_TYPE=json')

    path = os.path.join(config.outfile_dir, project_dir, 'project.config')
    with open(path, 'w') as file: 
        file.write("""project_title,purpose,is_longitudinal
"{}",{},{}
        """.format(project_name, 0, 1))

def write_form_events(api, project_name):
    event_map_path = os.path.join(config.outfile_dir, project_name, 'event_map.json')
    with open(event_map_path, 'r') as event_map:
        data = json.loads(event_map.read())

    form_events_path = os.path.join(config.outfile_dir, project_name, 'formEvents.xml')
    with open(form_events_path, 'w') as form_events_file:
        form_events_file.write(xml_util.form_events_render(data))

def write_translation_table(yaml_filename, project_name):
    yaml_path_in = os.path.join(config.infile_dir, yaml_filename)
    xml_filename = yaml_filename.replace('.yaml', '.xml')
    yaml_path_out = os.path.join(config.outfile_dir, project_name, xml_filename)
    with open(yaml_path_out, 'w') as yaml_file:
        yaml_file.write(xml_util.translation_table_render(yaml_path_in))


def main(argv):
    api = API(config.token, config.endpoint, config.versions[0])
    project_name = argv[1]
    if project_name:
        try:
            os.mkdir(os.path.join(config.outfile_dir, project_name))
        except:
            pass

        write_project_config(api, project_name)
        write_form_events(api, project_name)
        write_translation_table('translation.yaml', project_name)





if __name__ == "__main__":
    main(sys.argv)
