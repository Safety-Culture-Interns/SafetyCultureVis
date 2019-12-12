import requests
from flaskr import db
from threading import Thread


class API:
    def __init__(self, username="", token=0):
        self.MongoDB = db.Audits()
        self.username = username
        self.token = token
        self.url = "https://api.safetyculture.io"  # live site
        self.header = {'Authorization': 'Bearer {}'.format(self.token),
                       'Content-Type': 'application/json'}  # live site
        self.set_database_collection_name()

    def set_database_collection_name(self):
        self.MongoDB.set_collection_name(self.username)

    # syncs the mongodb with the api, adding only the new audits
    def sync_with_api(self):
        mongo_audit_ids = self.MongoDB.get_all('audit_id')
        mongo_audit_dates = self.MongoDB.get_all('modified_at')
        api_audits = self.get_api_audit_ids_mod_dates()[0]
        api_audit_dates = self.get_api_audit_ids_mod_dates()[1]
        new_ids = self.compare_api_database(mongo_audit_ids, api_audits)
        self.write_audits_to_db(new_ids)
        return True

    # loops through the ids from the api, and removes any from list if they are also in the mongo ids
    def compare_api_database(self, mongo_ids, api_ids):
        new_entries = []
        for audit_id in api_ids:
            if audit_id in mongo_ids:  # TODO: also check modification date
                continue
            else:
                new_entries.append(audit_id)
        print("{} items are going to be added to the database".format(len(new_entries)))
        return new_entries

    # returns a dict from the api
    def get_json(self, value):
        if value == "audits" or value == "templates":
            request = requests.get(url="{}/{}/search".format(self.url, value), headers=self.header)
        else:
            request = requests.get(url="{}/{}/{}".format(self.url, "audits", value), headers=self.header)
        data = request.json()
        return data

    def is_good_api_token(self, token=0):
        if token == 0:
            token = self.token
        header = {'Authorization': 'Bearer {}'.format(token),
                  'Content-Type': 'application/json'}
        request = requests.get(url="{}/audits/search".format(self.url), headers=header)
        if request.status_code == 200:
            return True
        else:
            return False

    # returns a list of audit ids[0], and modified dates[1]
    def get_api_audit_ids_mod_dates(self):
        audits_and_mod_dates = []
        audit_ids = []
        audit_mods = []
        audit_data = self.get_json('audits')
        for i in range(0, len(audit_data['audits'])):
            audit_ids.append(audit_data['audits'][i]['audit_id'])
            audit_mods.append(audit_data['audits'][i]['modified_at'])
        audits_and_mod_dates.append(audit_ids)
        audits_and_mod_dates.append(audit_mods)
        return audits_and_mod_dates

    # uses multi-threading to upload audits to database
    def write_audits_to_db(self, audit_ids):
        def do_a_bunch(count):
            item = self.get_json(audit_ids[count])
            self.MongoDB.write_one_to_mongodb(item)
            print("{} uploaded to Mongodb".format(count))

        for i in range(len(audit_ids)):
            t = Thread(target=do_a_bunch, args=(i,))
            t.start()
