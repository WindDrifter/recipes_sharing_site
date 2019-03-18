from ...database import mongo
import pytest
import mongomock
import json
import bson
import random
from faker import Faker
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from ..users.model import User
fake = Faker()
@pytest.fixture(autouse=True)
def reset_db():
    mongo.db.users.drop()


def generate_random_user(password=None):
    password = password or fake.password(length=13)
    return {
        "username": fake.user_name(),
        "password": password,
        "password_confirmation": password,
        "name": fake.name(),
        "email": fake.safe_email()
        }
def create_user(user_data=None):
    user_model = User()
    user_data = user_data or generate_random_user()
    user_model.new_user(data=user_data)
    return user_model.get(user_data["email"])

def get_cookie_and_token(client, login_data):
    rv = client.post('/api/users/login',data=json.dumps(login_data), content_type='application/json')
    loaded_data = bson.json_util.loads(rv.data)
    print(loaded_data)
    return {"access_csrf": loaded_data.get("access_csrf"),
            "refresh_csrf": loaded_data.get("refresh_csrf"),
            }

def generate_token(username):
    return create_access_token(identity=username)

class Test_users:

    def test_return_data_type(self, client):
        fake_user = generate_random_user()
        rv = client.post('/api/users', data=json.dumps(fake_user), content_type='application/json')
        assert isinstance(json.loads(rv.data), dict)

    def test_non_repeating_data(self, client):
        fake_user = generate_random_user()
        rv = client.post('/api/users', data=json.dumps(fake_user), content_type='application/json')
        assert (rv.status_code == 200)

        assert ("success" in json.loads(rv.data))

    def test_repeating_user(self, client):
        fake_user = generate_random_user()
        client.post('/api/users', data=json.dumps(fake_user), content_type='application/json')
        rv = client.post('/api/users', data=json.dumps(fake_user), content_type='application/json')
        assert (rv.status_code == 403)

    def test_ensure_password_is_encrypted(self, client):
        fake_user = generate_random_user()
        rv = client.post('/api/users', data=json.dumps(fake_user), content_type='application/json')
        user_data = mongo.db.users.find_one({"username": fake_user["username"]})
        assert(user_data["password"])
        assert(user_data["password"] != fake_user["password"])

    def test_ensure_id_is_returned(self, client):
        fake_user = generate_random_user()
        rv = client.post('/api/users', data=json.dumps(fake_user), content_type='application/json')
        user_data = mongo.db.users.find_one({"username": fake_user["username"]})
        assert(user_data["_id"])

    def test_no_password_entered(self, client):
        fake_user = generate_random_user()
        fake_user["password"] = ""
        rv = client.post('/api/users', data=json.dumps(fake_user), content_type='application/json')
        assert (rv.status_code == 403)

    def test_no_matching_password_entered(self, client):
        fake_user = generate_random_user()
        fake_user["password_confirmation"] = "aaaa" + fake_user["password"]
        rv = client.post('/api/users', data=json.dumps(fake_user), content_type='application/json')
        assert (rv.status_code == 403)

    def test_get_user(self, client):
        fake_user = generate_random_user(password="SomeRandomAmount")
        create_user(fake_user)
        user_id = user_data = mongo.db.users.find_one({"username": fake_user["username"]}).get("_id")
        login_data = {"username": fake_user["username"], "password": "SomeRandomAmount"}
        login_auth = get_cookie_and_token(client, login_data)
        token = login_auth.get('token')
        rv = client.get('/api/users/{}'.format(user_id), headers={"Authorization":"Bearer {}".format(token)})
        assert (json.loads(rv.data).get("username") == fake_user.get("username"))

    def test_update_user(self, client):
        fake_user = generate_random_user(password="SomeRandomAmount")
        create_user(fake_user)
        user_id = user_data = mongo.db.users.find_one({"username": fake_user["username"]}).get("_id")
        login_data = {"username": fake_user["username"], "password": "SomeRandomAmount"}
        login_auth = get_cookie_and_token(client, login_data)
        token = login_auth.get('access_csrf')
        new_data = {"name": "NEWNAME"}
        rv = client.post('/api/users/{}'.format(user_id), data=json.dumps(new_data), \
        content_type='application/json', headers={"content_type":'application/json', "X-CSRF-TOKEN": token})
        assert (json.loads(rv.data).get("name") == "NEWNAME")

    def test_remove_user(self, client):
        fake_user = generate_random_user(password="SomeRandomAmount")
        create_user(fake_user)
        user_id = user_data = mongo.db.users.find_one({"username": fake_user["username"]}).get("_id")
        login_data = {"username": fake_user["username"], "password": "SomeRandomAmount"}
        login_auth = get_cookie_and_token(client, login_data)
        token = login_auth.get('access_csrf')
        client.delete('/api/users/{}'.format(user_id), headers={"content_type":'application/json', "X-CSRF-TOKEN": token})
        assert(mongo.db.users.find_one({"_id": user_id}) is None)

    def test_login(self, client):
        fake_user = generate_random_user(password="SomeRandomAmount")
        create_user(fake_user)
        login_data = {"username": fake_user["username"], "password": "SomeRandomAmount"}
        rv = client.post('/api/users/login',data=json.dumps(login_data), content_type='application/json')
        assert(bson.json_util.loads(rv.data).get("login"))
        assert(rv.headers.getlist('Set-Cookie'))

    def test_get_current_user(self, client):
        fake_user = generate_random_user(password="SomeRandomAmount")
        create_user(fake_user)
        login_data = {"username": fake_user["username"], "password": "SomeRandomAmount"}
        login_auth = get_cookie_and_token(client, login_data)
        token = login_auth.get('access_csrf')
        rv = client.get('/api/users/current_user', headers={"content_type":'application/json', "X-CSRF-TOKEN": token})
        assert(bson.json_util.loads(rv.data).get("current_user") == fake_user.get("username"))
