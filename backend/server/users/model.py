import pymongo
import bson
import uuid
import datetime
from ..utils_folder.custom_exceptions import ParametersNotMatch,EmptyParameters,InvalidFormat
from ..utils_folder.utils import remove_html_tags, create_expiry_date
from ...database import mongo
from html.parser import HTMLParser
from bson.json_util import loads, dumps
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import IndexModel, ASCENDING, DESCENDING
from email_validator import validate_email, EmailNotValidError
from cerberus import Validator
from lxml.html.clean import Cleaner

user_schema = {'name': {'type': 'string'}, 'email': {'type': 'string'},
               'password':{'type': 'string'}, 'username': {'type': 'string'},
               'first_name':{'type': 'string'}, 'last_name':{'type': 'string'}
               }
user_validator = Validator(user_schema)


cleaner = Cleaner()
cleaner.javascript = True
cleaner.style = True

def check_and_create_index():
    if mongo.db.users.count_documents({}) == 0:
        mongo.db.users.create_index([("email",ASCENDING), ("username",ASCENDING)], unique=True)

class User:
    def __init__(self, user_id="", data={}, email="", username=""):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.check_and_create_index()
        self.data = data

    def verify_user(self, username_input="", user_id=""):
        id_used = self.user_id or user_id
        username = self.username or username_input
        return ObjectId(id_used) is self.get(username=username).get("_id")

    # generate password hash
    def hash_password(self, password):
        pw_hash = generate_password_hash(password)
        return pw_hash

    def remove(self,user_id=""):
        user_removed = mongo.db.users.find_one({"_id": bson.ObjectId(self.user_id)})
        mongo.db.users.delete_one({"_id": bson.ObjectId(self.user_id)})
        return user_removed

    # check enter entered password with stored password in hash
    def check_password(self, pw_hash, password):
        return check_password_hash(pw_hash, password)

    def validate_password(self, password="", password_confirmation=""):
        if password == "":
            raise EmptyParameters("Must enter password")
        elif password != password_confirmation:
            raise ParametersNotMatch("Password not match")
        else:
            return True

    # login user
    def login_user(self, email="", username="",password=""):
        user = self.get(email=email) or self.get(username=username)
        user_password = user["password"]
        return self.check_password(user_password, password)


    def check_and_create_index(self):
        if mongo.db.users.count_documents({}) == 0:
            mongo.db.users.create_index([("email",ASCENDING), ("username",ASCENDING)], unique=True)


    def new_user(self, data={}):
        try:
            new_data = self.generate_user_data(data=data)
            result = mongo.db.users.insert_one(new_data)
            return mongo.db.users.find_one({"_id": bson.ObjectId(result.inserted_id)}, {"password": 0})
        except pymongo.errors.DuplicateKeyError:
            return {"error": "email or username existed"}
        except ParametersNotMatch:
            return {"error": "Password not match"}
        except InvalidFormat:
            return {"error": "Invalid field detected"}
        except EmptyParameters:
            return {"error": "Password required"}

    def update(self, data={}):
        try:
            data = self.generate_user_data(data)
            print(data)
            result = mongo.db.users.update_one({"_id": bson.ObjectId(self.user_id)}, {"$set": data})
            return mongo.db.users.find_one({"_id": bson.ObjectId(self.user_id)})
        except ParametersNotMatch:
            return {"error": "Password not match"}
        except InvalidFormat:
            return {"error": "Invalid field detected"}


    def verify_and_hash_password(self, password="", password_confirmation=""):
        self.validate_password(password, password_confirmation)
        return self.hash_password(password)

    def generate_user_data(self, data={}):
        if data is None:
            return {"error": "empty value"}
        if self.user_id == "" or data.get("password") is not None:
            legit_password = self.verify_and_hash_password(data["password"], data["password_confirmation"])
            data["password"] = legit_password
            data.pop("password_confirmation")

        if data.get("email"):
            validate_email(data["email"])

        if not user_validator.validate(data):
            raise InvalidFormat("format not allow")
        for key, value in data.items():
            if isinstance(value, str):
                if key == "password" or key == "email":
                    pass
                new_value = remove_html_tags(value)
                data[key] = new_value

        return data

    def get(self, user_id="", email="", username=""):
        result = None
        if user_id:
            result = mongo.db.users.find_one({"_id": bson.ObjectId(user_id)})
        elif email:
            result = mongo.db.users.find_one({"email": email})
        elif username:
            result = mongo.db.users.find_one({"username": username})
        return result
