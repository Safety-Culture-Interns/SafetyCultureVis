import pymongo


class Users:
    def __init__(self):
        self.mongo_string = "mongodb+srv://matt-lewandowski:Postclip18@cluster0-tjdbw.mongodb.net/test?retryWrites=true&w=majority"
        self.database_name = 'iauditor'
        self.mango_client = pymongo.MongoClient(self.mongo_string)
        self.my_database = self.mango_client[self.database_name]
        self.db_collection_users = self.my_database['users']

    def add_user(self, username, password, api):
        result = self.db_collection_users.insert_one(
            {
                "username": username,
                "password": password,
                "api_number": api
            }
        )
        return result

    def correct_log_in(self, username, password):
        document = self.db_collection_users.find_one({'username': username, 'password': password})
        if document is None:
            return False
        else:
            return True

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
