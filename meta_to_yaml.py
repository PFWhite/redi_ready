#! /usr/bin/python3
import sys
import fileinput
import yaml
import json
import copy

forms = [
    'cbc_imported',
    'inr_imported',
    'chemistry_imported',
    'hcv_rna_imported'
]

def get_new_cc():
    clinical_component = {
        'l': 'UNKNOWN',
        'c': 'UNKNOWN',
        'f': 'redcap form name',
        'v': 'value name field',
        'u': 'unit name field',
    }
    return copy.copy(clinical_component)


def main(argv):
    lines = []
    for line in fileinput.input():
        lines.append(line)
    metadata = json.loads(''.join(lines))
    components = []

    curr_clinical_component = get_new_cc()

    for index, item in enumerate(metadata):
        if item['form_name'] in forms:
            curr_clinical_component['f'] = item['form_name']
            curr_clinical_component['v'] = item['field_name']
            curr_clinical_component['u'] = metadata[index+1]['field_name']
            curr_clinical_component['c'] = item['field_label']
            curr_clinical_component['field_label1'] = item['field_label']
            curr_clinical_component['field_label2'] = metadata[index+1]['field_label']
            curr_clinical_component['field_type1'] = item['field_type']
            curr_clinical_component['field_type2'] = metadata[index+1]['field_type']
            label1 = item['field_label']
            label2 = metadata[index+1]['field_label']
            components.append(curr_clinical_component)
            curr_clinical_component = get_new_cc()

    # components = [item for index, item in enumerate(components) if index % 3 == 0]

    yaml_text = yaml.dump({'components': components},
                          default_flow_style=False,
                          indent=4,
                          width=80)
    with open('outfile.yaml', 'w') as out_file:
        out_file.write(yaml_text)
    print('DONE')


if __name__ == "__main__":
    main(sys.argv)
