from jinja2 import Template
import yaml

template_paths = {
    'form_events': './xml_util/templates/formEvents.html',
    'translation_table': './xml_util/templates/translationTable.html'
}

templates = {}
for key in template_paths:
    with open(template_paths[key], 'r') as template_file:
        templates[key] = Template(template_file.read())

def form_events_render(event_map):
    forms = {}
    for item in event_map:
        form_name = item.get('form')
        if forms.get(form_name):
            pass
        else:
            forms[form_name] = {
                'name': form_name,
                'form_data_field': '!!!UNKNOWN!!!',
                'form_completed_field_name': '!!!UNKNOWN!!!',
                'form_completed_field_value': '!!!UNKNOWN!!!',
                'form_imported_field_name': '!!!UNKNOWN!!!',
                'form_imported_field_value': '!!!UNKNOWN!!!',
                'events': []
            }
        forms[form_name]['events'].append({'unique_event_name': item['unique_event_name']})
    # end events
    return templates['form_events'].render(forms=forms)


def translation_table_render(yaml_path):
    yaml_file = open(yaml_path, 'r')
    data = yaml.load(yaml_file.read())
    return templates['translation_table'].render(components=data['components'])

