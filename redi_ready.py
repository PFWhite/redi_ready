#! /usr/bin/python

import sys
import json
from cappy import API, beautify_json
import xml_util
import config

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
    write_project_config(api, 'test')

    path = '/'.join([config.outfile_dir, 'test', 'event_map.json'])
    with open(path, 'r') as event_map:
        data = json.loads(event_map.read())

    with open('/'.join([config.outfile_dir, 'test', 'formEvents.xml']), 'w') as form_events_file:
        form_events_file.write(xml_util.form_events_render(data))



if __name__ == "__main__":
    main(sys.argv)