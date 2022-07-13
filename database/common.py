from bson import ObjectId
from errors import InvalidObjectId

def get_ObjectId_if_valid(id, obj_name='id'):
    try:
        return ObjectId(id)
    except:
        raise InvalidObjectId('{} is invalid'.format(obj_name))