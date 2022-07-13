from datetime import timedelta
from functools import wraps
from flask import abort, request
from flask_jwt_extended import JWTManager, jwt_required, current_user
from flask_expects_json import expects_json
from errors import BadRequestError

from main import app
from user.modal import User
from user.util import registerReqSchema, signInReqSchema

ACCESS_EXPIRES = timedelta(hours=8)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES

jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):    
    # print(_jwt_header)    
    # print(jwt_data)
    user_id = jwt_data["sub"]
    return User.get_user_by_id(user_id)

@jwt.invalid_token_loader
def invalid_token(callback):
    return {
        'error': 'Invalid Authorization Token'
    }, 401
    # raise UnauthorizedError('Invalid Authorization Token')

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return {
        'error': 'Authorization token is missing in header'
    }, 401
    # raise UnauthorizedError('Authorization token is missing in header')




def admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        abort(403, 'Unauthorized Access!. Only admin can access this routes')
        
    return decorated_view


@app.route('/user/register', methods=['POST'])
@expects_json(registerReqSchema)
def signup():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin')

    user = User.sign_up(name, email, password, is_admin)
    return user.to_json_for_user(), 201
    

@app.route('/user/login', methods=["POST"])
@expects_json(signInReqSchema)
def sign_in():
    data = request.get_json()

    email = data['email']
    password = data['password']

    token = User.sign_in(email, password)
    return {
        'access_token' : token
    }, 200
    

@app.route('/user/profile', methods=["GET"])
@jwt_required()
def user_profile():

    user = current_user

    if user:
        return user.to_json_for_user()
    else:
        raise BadRequestError('User Not Found')        


@app.route('/user/logout', methods=['POST'])
@jwt_required
def user_sign_out():
    pass


@app.route('/user/delete', methods=["DELETE"])
@jwt_required()
def user_delete():
    user = current_user

    if user:
        user.delete_user()
        return {
            "message": "User Deleted"
        }, 200        
    else:
        raise BadRequestError('User Not Found')
        
    
    
