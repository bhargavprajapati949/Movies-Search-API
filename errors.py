from jsonschema import ValidationError
from werkzeug.exceptions import HTTPException, BadRequest
from http.client import HTTPException as HTTPExceptionFromHTTP
from pymongo.errors import PyMongoError

class InvalidObjectId(Exception):
    def __init__(self, message):
        self.message = message
        self.error_code = 400

class BadRequestError(Exception):
    def __init__(self, message='Bad Parameters'):
        self.message = message
        self.error_code = 400

class ServerError(Exception):
    def __init__(self, message='Internal Server Error'):
        self.message = message
        self.error_code = 500

def handle_exception(error):
    message = str(error)
    error_code = 500

    if isinstance(error, InvalidObjectId):
        message = error.message
        error_code = error.error_code

    elif isinstance(error, BadRequestError):
        message = error.message
        error_code = error.error_code

    elif isinstance(error, ServerError):
        message = error.message
        error_code = error.error_code

    elif isinstance(error, BadRequest):
        error_code = error.code
        message = error.description
        if isinstance(message, ValidationError):
            message = message.message
    
    elif isinstance(error, HTTPException):
        message = error.description
        error_code = error.code

    elif isinstance(error, PyMongoError):
        error_code = 500

    # elif isinstance(error, HTTPExceptionFromHTTP):
    
    print("From Error file")
    print(type(error))
    print(error)


    return {
        "error": message
    }, error_code
