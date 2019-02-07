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

recipes = Blueprint('recipes', __name__, url_prefix='/api/recipes')

@recipes.route('/', methods=['POST'])
@recipes.route('', methods=['POST'])
def create_recipe():

    pass
