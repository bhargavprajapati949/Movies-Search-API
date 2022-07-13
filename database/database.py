import os
from main import app

from flask_pymongo import PyMongo

app.config["MONGO_URI"] = os.environ.get('DB_URL')
mongo = PyMongo(app)

db = mongo.db

