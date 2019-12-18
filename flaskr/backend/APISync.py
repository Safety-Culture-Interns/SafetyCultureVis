from collections import OrderedDict

import requests

from flaskr import db
from threading import Thread
import time


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
        api_audits = self.get_api_audit_ids_mod_dates()[0]
        api_audit_dates = self.get_api_audit_ids_mod_dates()[1]
        self.delete_from_mongo(mongo_audit_ids, api_audits)
        mongo_audit_ids = self.MongoDB.get_all('audit_id')
        mongo_audit_dates = self.MongoDB.get_all('modified_at')
        mongo_zipped = list(map(list, zip(mongo_audit_ids, mongo_audit_dates)))
        api_zipped = list(map(list, zip(api_audits, api_audit_dates)))
        new_ids = self.compare_api_database(mongo_zipped, api_zipped)
        yield self.write_audits_to_db(new_ids)

    # loops through the ids from the api, and removes any from list if they are also in the mongo ids
    def compare_api_database(self, mongo_zipped, api_zipped):
        def filter_duplicate(item):
            if item in ll:
                return False
            else:
                return True

        ll = api_zipped
        out_filter = list(filter(filter_duplicate, mongo_zipped))
        ll = mongo_zipped
        out_filter += list(filter(filter_duplicate, api_zipped))
        try:
            audit_ids, audit_dates = zip(*out_filter)
            audits_to_add = list(OrderedDict.fromkeys(audit_ids))
            audits_to_delete = self.get_duplicates(audit_ids)
            print("audits to add {}".format(audits_to_add))
            print("audits to delete {}".format(audits_to_delete))
            for audit in audits_to_delete:
                self.MongoDB.delete_audit(audit)
            return audits_to_add
        except ValueError:
            print('Database and api are the same')
            return []

    def get_duplicates(self, audit_ids):
        duplicates = list(set([item for item in audit_ids if audit_ids.count(item) > 1]))
        return duplicates

    # deletes audits from database that are not in api
    def delete_from_mongo(self, mongo_ids, audit_ids):
        audit_ids_to_delete = list(filter(lambda x: x not in audit_ids, mongo_ids))
        for audit in audit_ids_to_delete:
            print("deleting {}".format(audit))
            self.MongoDB.delete_audit(audit)

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

        def thread():
            max_request = 200
            amount = len(audit_ids)
            count = 0
            threads = list()
            if len(audit_ids) == 0:
                yield 100
            while amount > max_request:

                for i in range(max_request):
                    t = Thread(target=do_a_bunch, args=(i,))
                    threads.append(t)
                    t.start()
                amount = amount - max_request
                for index, thread in enumerate(threads):
                    thread.join()
                    count += 1
                    print(count)
                    yield (count / len(audit_ids)) * 100
                time.sleep(60)
            for i in range(len(audit_ids) - count):
                t = Thread(target=do_a_bunch, args=(i,))
                threads.append(t)
                t.start()
            for index, thread in enumerate(threads):
                thread.join()
                count += 1
                yield (count / len(audit_ids)) * 100

        for done_thread in thread():
            yield done_thread
