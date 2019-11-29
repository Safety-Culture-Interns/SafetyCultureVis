import pymongo
import secrets

MONGOSTRING = "mongodb+srv://{}:{}@cluster0-tjdbw.mongodb.net/test?retryWrites=true&w=majority".format(
    secrets.get_database_user(), secrets.get_database_password())
COLLECTION_NAME = 'audits01'
DATABASE_NAME = 'iauditor01'
mango_client = pymongo.MongoClient(MONGOSTRING)
my_database = mango_client[DATABASE_NAME]
db_collection = my_database[COLLECTION_NAME]


def write_one_to_mongodb(data):
    x = db_collection.insert_one(data)


def write_many_to_mongodb(data):
    x = db_collection.insert_many(data)


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


def get_all(key):
    audit_ids = []
    document = db_collection.distinct(key)
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
