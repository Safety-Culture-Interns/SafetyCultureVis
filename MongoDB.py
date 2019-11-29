import pymongo
import csv
import secrets

MONGOSTRING = "mongodb+srv://{}:{}@cluster0-tjdbw.mongodb.net/test?retryWrites=true&w=majority".format(
    secrets.get_database_user(), secrets.get_database_password())
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
        if modified_doc.count() == 1:
            update_modified(data, modified_doc)  # TODO: make this work by using find_one()
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


def get_all_audit_ids():
    audit_ids = []
    document = db_collection.distinct('audit_id')
    for id in document:
        audit_ids.append(id)
    return audit_ids


def get_audit_information(audit_id, x):
    if isinstance(x, str):
        audit = db_collection.distinct(x, {'audit_id': audit_id})
        return audit[0]
    elif len(x) == 2:
        audit = db_collection.distinct('{}.{}'.format(x[0], x[1]), {'audit_id': audit_id})
        return audit[0]
    elif len(x) == 3:
        audit = db_collection.distinct('{}.{}.{}'.format(x[0], x[1], x[2]), {'audit_id': audit_id})
        return audit[0]
    elif len(x) == 5:
        audit = db_collection.distinct('{}.{}.{}.{}.{}'.format(x[0], x[1], x[2], x[3], x[4]), {'audit_id': audit_id})
        return audit
