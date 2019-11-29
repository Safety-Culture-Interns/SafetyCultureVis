import requests
import json
from audits import Template, Audits, Item
import WriteCsv
import MongoDB

URL = "https://api.safetyculture.io"  # live site
# URL = "https://sandpit-api.safetyculture.io"  # sand box
HEADER = {'Authorization': 'Bearer 9defde6335dd17c61959ae46a7d73a307c0945fbcd435dc649d1d341235e5105'}  # live site


# HEADER = {'Authorization': 'Bearer c9b02a45268c522719c457f46bec3a1f6142f1513191fee0204d5603689b80da'}  # sandbox


def main():
    # templates = create_templates()
    # audit_ids = create_audit_ids() #TODO: create new .py specifically for pulling from API to Database
    # write_audits_to_db(audit_ids)
    audit_ids = MongoDB.get_all_audit_ids()
    if MongoDB.get_database_length() > MongoDB.get_csv_length():
        audits = create_audits(audit_ids)
        WriteCsv.write_to_csv(audits)


def get_json(value):
    if value == "audits" or value == "templates":
        request = requests.get(url="{}/{}/search".format(URL, value), headers=HEADER)
    else:
        request = requests.get(url="{}/{}/{}".format(URL, "audits", value), headers=HEADER)
    data = request.json()
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
    data = get_json('audits')  # TODO: this needs to key all of the audit ids from the database
    audits = []
    blah = MongoDB.get_all_audit_ids()
    for number, list in enumerate(data['audits']):  # TODO: create a seperate fucntion/script that will update from api
        audit_id = data['audits'][number]['audit_id']
        # if not MongoDB.id_in_database(audit_id): #TODO: this is a very slow way of doing it. Bottle Neck!
        audits.append(audit_id)
    return audits


def write_audits_to_db(audit_ids):
    for i in range(0, len(audit_ids)):
        data = get_json(audit_ids[i])
        MongoDB.write_to_mongodb(data)


def create_audits(audit_ids):
    audits = []
    for i in range(0, MongoDB.get_database_length()):
        print(i)
        # data = get_json(audit_ids[i])
        data = MongoDB.get_all_from_db(audit_ids[i])
        audit_id = data['audit_id']

        audit_name = remove_special_characters(data['audit_data']['name'])
        owner_name = remove_special_characters(data['audit_data']['authorship']['owner'])
        template_owner = remove_special_characters(data['template_data']['authorship']['owner'])
        template_author = remove_special_characters(data['template_data']['authorship']['author'])
        template_description = remove_special_characters(data['template_data']['metadata']['description'])
        template_name = remove_special_characters(data['template_data']['metadata']['name'])

        template_id = MongoDB.get_audit_information(audit_id, 'template_id')
        archived = MongoDB.get_audit_information(audit_id, 'archived')
        created_on = MongoDB.get_audit_information(audit_id, ['audit_data', 'date_started'])
        modified_on = MongoDB.get_audit_information(audit_id, ['audit_data', 'date_modified'])
        score = MongoDB.get_audit_information(audit_id, ['audit_data', 'score'])
        total_score = MongoDB.get_audit_information(audit_id, ['audit_data', 'total_score'])
        score_percentage = MongoDB.get_audit_information(audit_id, ['audit_data', 'score_percentage'])
        audit_name = MongoDB.get_audit_information(audit_id, ['audit_data', 'name'])
        duration = MongoDB.get_audit_information(audit_id, ['audit_data', 'duration'])
        date_completed = MongoDB.get_audit_information(audit_id, ['audit_data', 'date_completed'])
        owner_name = MongoDB.get_audit_information(audit_id, ['audit_data', 'authorship', 'owner'])
        owner_id = MongoDB.get_audit_information(audit_id, ['audit_data', 'authorship', 'owner_id'])
        latitude = MongoDB.get_audit_information(audit_id, ['header_items', 'responses', 'location', 'geometry',
                                                            'coordinates'])[0]
        longitude = MongoDB.get_audit_information(audit_id, ['header_items', 'responses', 'location', 'geometry',
                                                             'coordinates'])[1]
        # working = False
        # count = 0
        # while not working:
        #     try:
        #         latitude = data['header_items'][count]['responses']['location']['geometry']['coordinates'][1]
        #         longitude = data['header_items'][count]['responses']['location']['geometry']['coordinates'][0]
        #         working = True
        #     except IndexError:
        #         count += 1
        #     except KeyError:
        #         count += 1
        #     if count == 8:
        #         working = True
        #         latitude = "none"
        #         longitude = "none"
        aud = Audits.Audit(audit_id, template_id, archived, created_on, modified_on, score, total_score,
                           score_percentage,
                           audit_name, duration, date_completed, owner_name, owner_id, latitude, longitude,
                           template_owner, template_author, template_description, template_name, template_owner_id,
                           template_author_id)
        audits.append(aud)
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


def remove_special_characters(text):
    return ''.join(e for e in text if e.isascii())


main()
