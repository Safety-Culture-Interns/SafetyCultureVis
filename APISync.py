import requests
import MongoDB
import secrets
import json
import csv
from audits import Audits
import application

URL = "https://api.safetyculture.io"  # live site
HEADER = {'Authorization': 'Bearer {}'.format(secrets.get_token()), 'Content-Type': 'application/json'}  # live site
CSV_FILE = 'data.csv'


# syncs the mongodb with the api, adding only the new audits
def sync_with_api():
    mongo_audit_ids = MongoDB.get_all('audit_id')
    mongo_audit_dates = MongoDB.get_all('modified_at')
    api_audits = get_api_audit_ids_mod_dates()[0]
    api_audit_dates = get_api_audit_ids_mod_dates()[1]
    new_ids = compare_api_database(mongo_audit_ids, api_audits)
    write_audits_to_db(new_ids)
    update_csv(new_ids)
    return True


# loops through the ids from the api, and removes any from list if they are also in the mongo ids
def compare_api_database(mongo_ids, api_ids):
    new_entries = []
    for audit_id in api_ids:
        if audit_id in mongo_ids:  # TODO: also check modification date
            continue
        else:
            new_entries.append(audit_id)
    print("{} items are going to be added to the database".format(len(new_entries)))
    return new_entries


# returns a dict from the api
def get_json(value):
    if value == "audits" or value == "templates":
        request = requests.get(url="{}/{}/search".format(URL, value), headers=HEADER)
    else:
        request = requests.get(url="{}/{}/{}".format(URL, "audits", value), headers=HEADER)
    data = request.json()
    return data


# returns a list of audit ids[0], and modified dates[1]
def get_api_audit_ids_mod_dates():
    audits_and_mod_dates = []
    audit_ids = []
    audit_mods = []
    audit_data = get_json('audits')
    for i in range(0, len(audit_data['audits'])):
        audit_ids.append(audit_data['audits'][i]['audit_id'])
        audit_mods.append(audit_data['audits'][i]['modified_at'])
    audits_and_mod_dates.append(audit_ids)
    audits_and_mod_dates.append(audit_mods)
    return audits_and_mod_dates


# gets json from iauditor api and writes it to mongodb
# if there are at least 10 audits left, it will bulk request and upload them
def write_audits_to_db(audit_ids):
    count = 0
    while (len(audit_ids) - count) != 0:
        if (len(audit_ids) - count) >= 10:
            ten_ids = []
            for x in range(0, 10):
                ten_ids.append(audit_ids[count + x])
            count += 10
            batch_write_to_db(ten_ids)
            print("{} uploaded to Mongodb".format(count))
        else:
            item = get_json(audit_ids[count])
            MongoDB.write_one_to_mongodb(item)
            count += 1
            print("{} uploaded to Mongodb".format(count))


def batch_write_to_db(ids):
    batch = {
        'requests': [
            {"method": "get", "path": "/audits/{}".format(ids[0])},
            {"method": "get", "path": "/audits/{}".format(ids[1])},
            {"method": "get", "path": "/audits/{}".format(ids[2])},
            {"method": "get", "path": "/audits/{}".format(ids[3])},
            {"method": "get", "path": "/audits/{}".format(ids[4])},
            {"method": "get", "path": "/audits/{}".format(ids[5])},
            {"method": "get", "path": "/audits/{}".format(ids[6])},
            {"method": "get", "path": "/audits/{}".format(ids[7])},
            {"method": "get", "path": "/audits/{}".format(ids[8])},
            {"method": "get", "path": "/audits/{}".format(ids[9])}
        ]
    }
    batch = json.dumps(batch)
    request = requests.post(url="{}/{}".format(URL, 'batch'), headers=HEADER, data=batch)
    data = request.json()
    MongoDB.write_many_to_mongodb(data)


# takes a list of new or updated audits and writes them to the csv file
def update_csv(new_entries):
    csv_data = []
    with open(CSV_FILE, mode='r') as old_csv_file:
        csv_reader = csv.DictReader(old_csv_file)
        line_count = 0
        for i, row in enumerate(csv_reader):
            if line_count == 0:
                csv_data = [["audit_id", "template_id", "audit_created_at_date", "audit_created_at_time",
                             "audit_modified_at_date", "audit_modified_at_time", "score", "total_score",
                             "score_percentage",
                             "audit_name", "duration", "date_completed_date", "date_completed_time", "owner_name",
                             "owner_id",
                             "longitude", "latitude", "template_owner", "template_author", "template_description",
                             "template_name",
                             "template_owner_id", "template_author_id"]]
                line_count += 1

            if row["audit_id"] not in new_entries:
                csv_data.append([row.get("audit_id"), row["template_id"], row["audit_created_at_date"],
                                 row["audit_created_at_time"], row["audit_modified_at_date"],
                                 row["audit_modified_at_time"], row["score"], row["total_score"],
                                 row["score_percentage"], row["audit_name"], row["duration"],
                                 row["date_completed_date"], row["date_completed_time"], row["owner_name"],
                                 row["owner_id"], row["longitude"], row["latitude"], row["template_owner"],
                                 row["template_author"], row["template_description"], row["template_name"],
                                 row["template_owner_id"], row["template_author_id"]])

    new_audits = create_audits(new_entries)
    for audit in new_audits:
        created_at = audit.get_audit_created_at()
        modified_at = audit.get_audit_modified_at()
        completed_at = audit.get_date_completed()

        if created_at is None:
            created_date = ""
            created_time = ""
        else:
            created_date = created_at[:10]
            created_time = created_at[11:-5]

        if modified_at is None:
            modified_at_date = ""
            modified_at_time = ""
        else:
            modified_at_date = modified_at[:10]
            modified_at_time = modified_at[11:-5]

        if completed_at is None:
            completed_at_date = ""
            completed_at_time = ""
        else:
            completed_at_date = completed_at[:10]
            completed_at_time = completed_at[11:-5]

        csv_data.append([audit.get_audit_id(), audit.get_template_id(),
                         created_date, created_time,
                         modified_at_date, modified_at_time,
                         audit.get_score(), audit.get_total_score(),
                         audit.get_score_percentage(), audit.get_audit_name(),
                         audit.get_duration(), completed_at_date,
                         completed_at_time, audit.get_owner_name(),
                         audit.get_owner_id(), audit.get_longitude(),
                         audit.get_latitude(), audit.get_template_owner(),
                         audit.get_template_author(), audit.get_template_description(),
                         audit.get_template_name(), audit.get_template_owner_id(),
                         audit.get_template_author_id()])

    with open(CSV_FILE, 'w', newline='') as new_csv_file:
        writer = csv.writer(new_csv_file)
        writer.writerows(csv_data)
    new_csv_file.close()


def create_audits(audit_ids):
    audits = []
    for i in range(0, len(audit_ids)):
        print("{} audit added to class list".format(i))
        data = MongoDB.get_all_from_db(audit_ids[i])
        audit_id = data['audit_id']
        template_id = MongoDB.get_audit_information(audit_id, 'template_id')
        template_data = MongoDB.get_audit_information(audit_id, 'template_data')
        audit_data = MongoDB.get_audit_information(audit_id, 'audit_data')
        template_owner = remove_special_characters(template_data['authorship']['owner'])
        template_author = remove_special_characters(template_data['authorship']['author'])
        template_description = remove_special_characters(template_data['metadata']['description'])
        template_name = remove_special_characters(template_data['metadata']['name'])
        template_author_id = template_data['authorship']['author_id']
        template_owner_id = template_data['authorship']['owner_id']
        created_on = audit_data['date_started']
        modified_on = audit_data['date_modified']
        score = audit_data['score']
        total_score = audit_data['total_score']
        score_percentage = audit_data['score_percentage']
        audit_name = remove_special_characters(audit_data['name'])
        duration = audit_data['duration']
        date_completed = audit_data['date_completed']
        owner_name = remove_special_characters(audit_data['authorship']['owner'])
        owner_id = audit_data['authorship']['owner_id']
        try:
            coordinates = MongoDB.get_audit_information(audit_id, ['header_items', 'responses', 'location', 'geometry',
                                                                   'coordinates'])
            latitude = coordinates[0]
            longitude = coordinates[1]
        except IndexError:
            latitude = ''
            longitude = ''
        aud = Audits.Audit(audit_id, template_id, created_on, modified_on, score, total_score,
                           score_percentage,
                           audit_name, duration, date_completed, owner_name, owner_id, latitude, longitude,
                           template_owner, template_author, template_description, template_name, template_owner_id,
                           template_author_id)
        audits.append(aud)
    return audits


# removes non ascii characters from a string
def remove_special_characters(text):
    return ''.join(e for e in text if e.isascii())


# returns the number of lines in the csv.
# used to determine if csv needs to be updates
def get_csv_length():
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = sum(1 for row in csv_reader)
        return row_count
