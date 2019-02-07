from ...database import mongo
import pytest
import mongomock
import json
import bson
import random
from faker import Faker
fake = Faker()
@pytest.fixture(autouse=True)
def reset_db():
    mongo.db.items.drop()
