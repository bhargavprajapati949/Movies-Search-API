from database.common import get_ObjectId_if_valid
from database.database import db

users = db.users

def add_user(user):
    return users.insert_one(user)

def find_user_by_id(user_id : str):
    obj_id = get_ObjectId_if_valid(user_id, 'User id')
    return users.find_one(obj_id)
    

def find_user_by_email(email):
    return users.find_one({"email": email})

def delete_user(user_id: str):
    obj_id = get_ObjectId_if_valid(user_id, 'User id')
    return users.delete_one({ "_id": obj_id})
    

    