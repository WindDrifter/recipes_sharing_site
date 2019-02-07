import os
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_pymongo import PyMongo
from flask import Blueprint, render_template, abort
    # create and configure the app
from .database import mongo
from .server.users import routes as user_router
# from .server.posts import routes as post_router
jwt = None
def create_app(test_config=None, testing=False):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # change this to using enviroment variable
    app.config['JWT_SECRET_KEY'] = "puddi"
    if test_config is None and not testing:
        # load the instance config, if it exists, when not testing
        app.config["MONGO_URI"] = "mongodb://localhost:27017/recetteApp"
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config["MONGO_URI"] = "mongodb://localhost:27017/recetteApp"
        if test_config:
            app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.register_blueprint(user_router.users)
    # app.register_blueprint(post_router.posts)

    @app.route('/<path:page>')
    def fallback(page):
        return render_template('index.html')
    mongo.init_app(app)
    jwt = JWTManager(app)
    return app
