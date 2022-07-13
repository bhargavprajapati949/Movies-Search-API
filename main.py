import json
import os
from bson import ObjectId
from werkzeug.exceptions import HTTPException

from flask import Flask
from errors import handle_exception

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')


class JSONEncoder(json.JSONEncoder):
    ''' extending json-encoder class'''

    def default(self, o):
        if isinstance(o, ObjectId):
            ''' Converting ObjectId to string for serialization '''
            return str(o)
        if isinstance(o, set):
            ''' Converting set to list for serialization '''
            return list(o)
        return json.JSONEncoder.default(self, o)

app.json_encoder = JSONEncoder


app.register_error_handler(Exception, handle_exception)
