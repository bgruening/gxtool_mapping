from urllib.request import urlopen
import json
import csv

# Fetching JSON from Galaxy API
url = "https://usegalaxy.eu/api/tools"
response = urlopen(url)
data_json = json.loads(response.read())

missing_dict = []

with open('galaxy_tools_missing_in_biotools.tsv', 'wt') as out_file:
    # Initializing csv
    tsv_writer = csv.writer(out_file, delimiter='\t')
    # Adding table header
    tsv_writer.writerow(['name', 'id', 'description', 'tool_shed_repository', 'panel_section_name'])
    for section in data_json:
        if 'elems' in section:
            print(f"--- {section['name']} ---")
            for tool in section['elems']:
                biotools_check = False
                # Only tools
                if tool['model_class'] == 'Tool': 
                    # Checking if tool is in Bio.tools
                    if 'xrefs' in tool and tool['xrefs']:
                        for xref in tool['xrefs']:
                            if xref['reftype'] == "bio.tools":
                                biotools_check = True
                    if not biotools_check and 'tool_shed_repository' in tool:
                        # Writing row to table
                        tsv_writer.writerow([tool['name'], tool['id'], tool['description'],
                                             tool['tool_shed_repository']['name'], tool['panel_section_name']])
                        # Adding info tool to dictionary
                        missing_dict.append({'name': tool['name'], 'id': tool['id'], 'description': tool['description'],
                                             'tool_shed_repository': tool['tool_shed_repository']['name'], 'panel_section_name': tool['panel_section_name']})
                    else:
                        # Tool is already in Bio.tools
                        print(f"skipping {tool['name']}")

# Writing dictionary with missing tools to JSON
with open('galaxy_tools_missing_in_biotools.json', 'w', encoding='utf8') as json_file:
    json.dump(missing_dict, json_file, indent=4)
