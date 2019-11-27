import requests
import json
from audits import Template, Audits, Item

# URL = "https://api.safetyculture.io" #live site
URL = "https://sandpit-api.safetyculture.io"  # sand box
# HEADER = {'Authorization': 'Bearer 9defde6335dd17c61959ae46a7d73a307c0945fbcd435dc649d1d341235e5105'} # live site
HEADER = {'Authorization': 'Bearer c9b02a45268c522719c457f46bec3a1f6142f1513191fee0204d5603689b80da'}  # sandbox


def main():
    templates = create_templates()
    audit_ids = create_audit_ids()
    audits = create_audits(audit_ids)


def get_json(value):
    if value == "audits" or value == "templates":
        r = requests.get(url="{}/{}/search".format(URL, value), headers=HEADER)
    else:
        r = requests.get(url="{}/{}/{}".format(URL, "audits", value), headers=HEADER)
    data = r.json()
    return data


def create_templates():
    data = get_json('templates')
    templates = []
    for number, list in enumerate(data['templates']):
        template_id = list['template_id']
        try:
            template_name = list['name']
        except KeyError:
            template_name = "No Name"
        template_created_at = list['created_at']
        template_modified_on = list['modified_at']
        template = Template.Template(template_name, template_id, template_created_at, template_modified_on)
        templates.append(template)
    return templates


def create_audit_ids():
    data = get_json('audits')
    audits = []
    for number, list in enumerate(data['audits']):
        audit_id = data['audits'][number]['audit_id']
        audits.append(audit_id)
    return audits


def create_audits(audit_ids):
    audits = []
    # items = []
    # for audit in audit_ids:
    for i in range(0, 1):
        data = get_json(audit_ids[i])
        audit_id = data['audit_id']
        template_id = data['template_id']
        archived = data['archived']
        created_on = data['audit_data']['date_started']
        modified_on = data['audit_data']['date_modified']
        score = data['audit_data']['score']
        total_score = data['audit_data']['total_score']
        score_percentage = data['audit_data']['score_percentage']
        audit_name = data['audit_data']['name']
        duration = data['audit_data']['duration']
        date_completed = data['audit_data']['date_completed']
        owner_name = data['audit_data']['authorship']['owner']
        owner_id = data['audit_data']['authorship']['owner_id']
        latitude = data['header_items'][6]['responses']['location']['geometry']['coordinates'][0]
        longitude = data['header_items'][6]['responses']['location']['geometry']['coordinates'][1]
        aud = Audits.Audit(audit_id, template_id, archived, created_on, modified_on, score, total_score,
                           score_percentage,
                           audit_name, duration, date_completed, owner_name, owner_id, latitude, longitude)
        audits.append(aud)
        print(latitude)
        print(longitude)
    return audits


def create_items(data):
    item_ids = []
    item_labels = []
    item_types = []
    item_combined_scores = []
    item_max_scores = []
    item_parent_ids = []
    for item in data['items']:
        item_ids.append((json.dumps(item['item_id'])))
        item_labels.append((json.dumps(item['label'])))
        item_types.append((json.dumps(item['type'])))
        try:
            item_combined_scores.append((json.dumps(item['scoring']['combined_score'])))
        except KeyError:
            item_combined_scores.append(0)
        try:
            item_max_scores.append((json.dumps(item['scoring']['combined_max_score'])))
        except:
            item_max_scores.append(0)
        try:
            item_parent_ids.append((json.dumps(item['parent_id'])))
        except KeyError:
            item_parent_ids.append("0")
    for item_label in item_labels:
        print(item_label)
    return 4


main()
