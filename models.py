import pymongo
from flask_bcrypt import Bcrypt


class Users:
    def __init__(self):
        self.mongo_string = "mongodb+srv://safety-culture:Password12@cluster0-tjdbw.mongodb.net/test?retryWrites=true&w=majority"
        self.database_name = 'iauditor'
        self.mango_client = pymongo.MongoClient(self.mongo_string)
        self.my_database = self.mango_client[self.database_name]
        self.db_collection_users = self.my_database['users']
        self.bcrypt = Bcrypt(None)

    def add_user(self, username, password, api):
        result = self.db_collection_users.insert_one(
            {
                "_id": username,
                "password": self.hash_password(password),
                "api_number": api
            }
        )
        return result

    def hash_password(self, password):
        return self.bcrypt.generate_password_hash(password)

    def login(self, user_name, user_pass):
        if self.db_collection_users.find({"_id": user_name}).count() == 0:
            logged_in = False
        else:
            cursor = self.db_collection_users.find_one({"_id": user_name})
            password = self.bcrypt.check_password_hash(cursor['password'], user_pass)
            if password:
                logged_in = True
            else:
                logged_in = False
        return logged_in

    def user_exists(self, username):
        document = self.db_collection_users.find_one({'_id': username})
        if document is None:
            return False
        else:
            return True

    def get_password(self, username, api):
        try:
            document = self.db_collection_users.find_one({'_id': username, 'api_number': api})
            return document['password']
        except KeyError:
            return "Invalid username or api number"
        except TypeError:
            return "Invalid username or api number"
