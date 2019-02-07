import functools
from .model import *
from flask import (
    Blueprint, flash, g, jsonify,
    redirect, render_template, request, session, url_for
)
from ...database import mongo
from ..utils_folder.custom_exceptions import ParametersNotMatch,EmptyParameters,InvalidFormat

from flask import Response
import json
import bson
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)

users = Blueprint('users', __name__, url_prefix='/api/users')

@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_model = User()
    print(data.get("username"))
    result = user_model.login_user(email=data.get("email"), \
    username= data.get("username"), password = data.get("password"))
    if result:
        # store session
        username = data.get("username")
        email = data.get("email")
        user = user_model.get(username=username) or user_model.get(email=email)
        access_token = create_access_token(identity=user.get("username"))
        return jsonify({"token": access_token}), 200

    return jsonify({"message": "bad username, email or password"}), 400

@users.route('/logout', methods=['POST'])
@jwt_required
def logout():
    # clear session
    current_user = get_jwt_identity()
    return ""

@users.route('/current_user', methods=['GET'])
@jwt_required
def current_user():
    # clear session
    current_user = get_jwt_identity()
    print(current_user)
    return jsonify({"current_user":current_user}), 200


@users.route('/<user_id>', methods=['POST', 'GET', 'DELETE'])
@jwt_required
def get_user(user_id):
    current_user = get_jwt_identity()
    user_model = User(user_id=user_id)
    try:
        if request.method == "POST":
            data = request.get_json()
            user = user_model.update(data=data)
        elif request.method == 'DELETE':
            user = user_model.remove()
        else:
            user = user_model.get(user_id=user_id)
            user.pop("password")
        js = bson.json_util.dumps(user)
        resp = Response(js, status=200, mimetype='application/json')
        return resp
    except:
        return jsonify({"message": "Cannot access route"}), 403


@users.route('/', methods=['GET'])
def get_all_users():
    amount_limit = request.args.get('limit')
    js = json.dumps({"users": [1,3,4,6,7]})

    resp = Response(js, status=200, mimetype='application/json')
    # resp.headers['Access-Control-Allow-Origin']
    return resp


@users.route('/register', methods=['POST'])
@users.route('', methods=['POST'])
def register():
    if request.method == "POST":
        data = request.get_json()
        user_model = User()
        user = user_model.new_user(data=data)

        if "username" in user:
            status_code = 200
        else:
            status_code = 403
        js = bson.json_util.dumps(user)
        resp = Response(js, status=status_code, mimetype='application/json')

        return resp