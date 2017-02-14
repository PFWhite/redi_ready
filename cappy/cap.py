import json
import copy

import requests as req

import cappy.utils as utils

class API(object):

    def _add_iterable(self, iterable, name, post_body):
        for index, item in enumerate(iterable):
            post_body['{}[{}]'.format(name, index)] = item
        return post_body

    def _build_post_body(self, token, data, forms, fields, post_body):
            post_body['token'] = token
            if data:
                post_body['data'] = data
            if post_body.get('fields'):
                del post_body['fields']
                post_body = self._add_iterable(fields, 'field', post_body)
            if post_body.get('forms'):
                del post_body['forms']
                post_body = self._add_iterable(forms, 'form', post_body)
            return post_body

    def _redcap_call_from_def(self, token, endpoint, key):
        def run_call(data=None, forms=[], fields=[]):
            data_copy = copy.copy(self.api_definition[key])
            body = self._build_post_body(token, data, forms, fields, data_copy)
            return req.post(endpoint, body)
        return run_call

    def __init__(self, token, endpoint, version_file):
        version_path = utils.path_for_version(version_file)
        with open(version_path, 'r') as api_def:
            self.api_definition = json.loads(api_def.read())
        for key in self.api_definition:
            setattr(self, key, self._redcap_call_from_def(token, endpoint, key))
