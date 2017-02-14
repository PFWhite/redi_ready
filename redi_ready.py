#! /usr/bin/python

import sys
import json
from cappy import API, beautify_json
import xml_util
import config
import os

def save_response(project_dir, filename, content):
    path = '/'.join([config.outfile_dir, project_dir, filename])
    with open(path, 'w') as outfile:
        outfile.write(beautify_json(content))

def write_project_config(api, project_dir):
    save_response(project_dir, 'event.json', api.export_events().content)
    save_response(project_dir, 'instruments.json', api.export_instruments().content)
    save_response(project_dir, 'event_map.json', api.export_instrument_event_mapping().content)
    save_response(project_dir, 'metadata.json', api.export_metadata().content)
    save_response(project_dir, 'project.info', api.export_project_info().content)

    path = '/'.join([config.outfile_dir, project_dir, 'admin_user.token'])
    with open(path, 'w') as file:
        file.write(config.token)

    path = '/'.join([config.outfile_dir, project_dir, 'settings.ini'])
    with open(path, 'w') as file:
        file.write('IMPORT_CONTENT_TYPE=json')


def main(argv):
    api = API(config.token, config.endpoint, config.versions[0])
    project_name = argv[1]
    if project_name:
        try:
            os.mkdir(os.path.join(config.outfile_dir, project_name))
        except:
            pass

        write_project_config(api, project_name)

        path = os.path.join(config.outfile_dir, project_name, 'event_map.json')
        with open(path, 'r') as event_map:
            data = json.loads(event_map.read())

        with open(os.path.join(config.outfile_dir, project_name, 'formEvents.xml'), 'w') as form_events_file:
            form_events_file.write(xml_util.form_events_render(data))

        with open(os.path.join(config.outfile_dir, project_name, 'translationTable.xml'), 'w') as trans_file:
            trans_file.write(xml_util.translation_table_render('./xml_util/translation.yaml'))



if __name__ == "__main__":
    main(sys.argv)
