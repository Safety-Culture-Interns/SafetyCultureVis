import pymongo
import csv
from bson.json_util import dumps
import json
from bson import json_util
from bson import BSON

MONGOSTRING = "mongodb+srv://matt-lewandowski:Postclip18@cluster0-tjdbw.mongodb.net/test?retryWrites=true&w=majority"
COLLECTION_NAME = 'audits'
DATABASE_NAME = 'iauditor'
mango_client = pymongo.MongoClient(MONGOSTRING)
my_database = mango_client[DATABASE_NAME]
db_collection = my_database[COLLECTION_NAME]


def write_to_mongodb(data):
    if check_if_exists(data):
        print("already exists")
    else:
        x = db_collection.insert_one(data)


def check_if_exists(data):
    audit_id = data['audit_id']
    modified_on = data['audit_data']['date_modified']
    document = db_collection.find({'audit_id': audit_id})
    if document.count() == 1:
        modified_doc = db_collection.find({'modified_at': modified_on})
        if modified_doc.count() == 0:
            update_modified(data, modified_doc)
            return True
        return True
    return False


def update_modified(data, x):
    db_collection.remove(x)
    x = db_collection.insert_one(data)


def id_in_database(audit_id):
    document = db_collection.find({'audit_id': audit_id})
    if document.count() == 1:
        return True
    return False


def get_all_from_db(audit_id):
    document = db_collection.find_one({'audit_id': audit_id})
    return document


def get_database_length():
    document = db_collection.find()
    return document.count()

# returns the number of lines in the csv.
# used to determine if csv needs to be updates
def get_csv_length():
    with open('data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = sum(1 for row in csv_reader)
        return row_count
