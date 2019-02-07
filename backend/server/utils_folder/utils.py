import re
from bson import ObjectId
from cerberus import Validator
TAG_RE = re.compile(r'<[^>]+>')

def remove_html_tags(input_string=""):
    return_value = TAG_RE.sub("", input_string)
    return return_value

import datetime

def create_expiry_date(days=30):
    return datetime.datetime.now() + datetime.timedelta(days=days)


class ObjectIDValidator(Validator):
    def _validate_type_objectid(self, field, value):
        if not re.match('[a-f0-9]{24}', value):
            self._error(field, ERROR_BAD_TYPE.format('ObjectId'))
