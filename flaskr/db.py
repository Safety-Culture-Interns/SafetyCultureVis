import pymongo
from flask_bcrypt import Bcrypt

MONGOSTRING = "mongodb+srv://safety-culture:Password12@cluster0-tjdbw.mongodb.net/test?retryWrites=true&w=majority"


class Audits:
    def __init__(self):
        self.mongo_string = MONGOSTRING
        self.database_name = 'iauditor'
        self.mango_client = pymongo.MongoClient(self.mongo_string)
        self.my_database = self.mango_client[self.database_name]
        self.db_collection = self.my_database['audits']

    def set_collection_name(self, username):
        self.db_collection = self.my_database['audits-{}'.format(username)]

    def write_one_to_mongodb(self, data):
        x = self.db_collection.insert_one(data)

    def write_many_to_mongodb(self, data):
        x = self.db_collection.insert_many(data)

    def update_modified(self, data, x):
        self.db_collection.remove(x)
        x = self.db_collection.insert_one(data)

    def id_in_database(self, audit_id):
        document = self.db_collection.find({'audit_id': audit_id})
        if document.count() == 1:
            return True
        return False

    def get_all_from_db(self, audit_id):
        document = self.db_collection.find_one({'audit_id': audit_id})
        return document

    def get_database_length(self):
        document = self.db_collection.find()
        return document.count()

    def get_all(self, key):
        audit_ids = []
        document = self.db_collection.distinct(key)
        for id in document:
            audit_ids.append(id)
        return audit_ids

    def get_audit_information(self, audit_id, x):
        if isinstance(x, str):
            audit = self.db_collection.distinct(x, {'audit_id': audit_id})
            return audit[0]
        elif len(x) == 2:
            audit = self.db_collection.distinct('{}.{}'.format(x[0], x[1]), {'audit_id': audit_id})
            return audit[0]
        elif len(x) == 3:
            audit = self.db_collection.distinct('{}.{}.{}'.format(x[0], x[1], x[2]), {'audit_id': audit_id})
            return audit[0]
        elif len(x) == 5:
            audit = self.db_collection.distinct('{}.{}.{}.{}.{}'.format(x[0], x[1], x[2], x[3], x[4]),
                                                {'audit_id': audit_id})
            return audit


class Users:
    def __init__(self):
        self.mongo_string = MONGOSTRING
        self.database_name = 'iauditor'
        self.mango_client = pymongo.MongoClient(self.mongo_string)
        self.my_database = self.mango_client[self.database_name]
        self.db_collection_users = self.my_database['users']
        self.bcrypt = Bcrypt(None)

    def update_api(self, username, api):
        self.db_collection_users.find_and_modify({
            "query": {'username': username},
            "update": {'$set': {'api_number': api}}
        })

    def add_user(self, username, password, api):
        result = self.db_collection_users.insert_one(
            {
                "username": username,
                "password": self.hash_password(password),
                "api_number": api
            }
        )
        return result

    # returns the api for a certain username
    def get_api(self, username):
        return self.db_collection_users.distinct('api_number', {"username": username})[0]

    def get_user(self, username, user_pass):
        if self.user_exists(username):
            record = self.db_collection_users.find_one({"username": username})
            password = self.bcrypt.check_password_hash(record['password'], user_pass)
            if password:
                return record
            else:
                return None
        else:
            return None

    def get_user_by_id(self, id):
        return self.db_collection_users.find_one({'_id': id})

    def hash_password(self, password):
        return self.bcrypt.generate_password_hash(password)

    def login(self, user_name, user_pass):
        if self.db_collection_users.find({"username": user_name}).count() == 0:
            logged_in = False
        else:
            cursor = self.db_collection_users.find_one({"username": user_name})
            password = self.bcrypt.check_password_hash(cursor['password'], user_pass)
            if password:
                logged_in = True
            else:
                logged_in = False
        return logged_in

    def user_exists(self, username):
        document = self.db_collection_users.find_one({'username': username})
        if document is None:
            return False
        else:
            return True

    def get_password(self, username, api):
        try:
            document = self.db_collection_users.find_one({'username': username, 'api_number': api})
            return document['password']
        except KeyError:
            return "Invalid username or api number"
        except TypeError:
            return "Invalid username or api number"
