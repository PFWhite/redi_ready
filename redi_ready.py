#! /usr/bin/python

import sys
from cappy import API, beautify_json
import config

def save_response(filename, content):
    path = '/'.join([config.outfile_dir, filename])
    with open(path, 'w') as outfile:
        outfile.write(beautify_json(content))

def main(argv):
    api = API(config.token, config.endpoint, config.versions[0])

    print('getting, saving events')
    save_response('event.json', api.export_events().content)
    print('getting, saving instruments')
    save_response('instruments.json', api.export_instruments().content)
    print('getting, saving instrument event mapping')
    save_response('instrument_event_mapping.json', api.export_instrument_event_mapping().content)
    print('getting, saving metadata')
    save_response('metadata.json', api.export_metadata().content)

if __name__ == "__main__":
    main(sys.argv)
