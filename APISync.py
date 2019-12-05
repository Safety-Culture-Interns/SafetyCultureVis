import requests
import MongoDB
import secrets
import json

URL = "https://api.safetyculture.io"  # live site
HEADER = {'Authorization': 'Bearer {}'.format(secrets.get_token()), 'Content-Type': 'application/json'}  # live site


# syncs the mongodb with the api, adding only the new audits
def sync_with_api():
    mongo_audit_ids = MongoDB.get_all('audit_id')
    mongo_audit_dates = MongoDB.get_all('modified_at')
    api_audits = get_api_audit_ids_mod_dates()[0]
    api_audit_dates = get_api_audit_ids_mod_dates()[1]
    new_ids = compare_api_database(mongo_audit_ids, api_audits)
    write_audits_to_db(new_ids)


# loops through the ids from the api, and removes any from list if they are also in the mongo ids
def compare_api_database(mongo_ids, api_ids):
    list = []
    for id in api_ids:
        if id in mongo_ids:  # TODO: also check modification date
            continue
        else:
            list.append(id)
    print("{} items are going to be added to the database".format(len(list)))
    return list


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
