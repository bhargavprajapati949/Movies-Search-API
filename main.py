import json
import os
from bson import ObjectId

from flask import Flask, redirect
from errors import handle_exception

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')

@app.route("/", methods=['GET'])
def homepage():
    return redirect("https://github.com/bhargavprajapati949/Movies-Search-API")
    # return "This is my homepage"

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
