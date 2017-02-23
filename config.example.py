import os
from cappy import get_version_files

token = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
endpoint = 'https://dev.redcap.org/api/'

versions = get_version_files()

outfile_dir = os.path.join('.', 'data')
infile_dir = os.path.join('.', 'data_in')

def get_settings_ini_path(project_dir):
    return os.path.join(outfile_dir, project_dir, 'settings.ini')
settings_ini_string = 'IMPORT_CONTENT_TYPE={}'

def get_project_config_path(project_dir):
    return os.path.join(outfile_dir, project_dir, 'project.config')
project_config_string = """project_title,purpose,is_longitudinal
"{}",{},{}"""
