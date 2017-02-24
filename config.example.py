import os
from cappy import get_version_files

source_project = {
    'token': 'xxxxxxxxxxxxxxxxxxx',
    'endpoint': 'https://source.redcap.org/api/'
}

target_project = {
    'endpoint': 'http://target.recap.dev/redcap/api/',
    'super_token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
}

versions = get_version_files()

fetch_data = True
# fetch_data = False

push_data = True
# push_data = False

outfile_dir = os.path.join('.', 'data')
infile_dir = os.path.join('.', 'data_in')

