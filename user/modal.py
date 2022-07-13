from flask import escape
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

import database.user as db_users
from errors import BadRequestError, ServerError


class User():
    def __init__(self, name, email, hashed_password = None, id=None, is_admin=False):
        super().__init__()
        self.id = id        # string
        self.name = name       
        self.email = email     
        self.__hashed_password = hashed_password
        self.is_admin = is_admin

    @staticmethod
    def sign_up(name, email, password):

        if User.get_user_by_email_if_exist(email):            
            raise Exception("Account with email {} is already exist".format(escape(email)))

        user = User(
            name=name,
            email=email,
            hashed_password=User.get_hashed_password(password)
        )
        
        user = db_users.add_user(user.__to_json_for_db())
        if user:
            return User.get_user_by_id(user.inserted_id)

        raise ServerError('SignUp Failed')

    @staticmethod
    def sign_in(email, password):
        
        user = User.get_user_by_email_if_exist(email)

        if user and user.verify_hashed_password(password):
            token = create_access_token(identity=user.id)
            return token
        
        raise BadRequestError('Username does not exist or password is wrong')

    def delete_user(self):
        res =  db_users.delete_user(self.id)
        if res.deleted_count == 1:
            return True
        else:
            raise ServerError('Unable to delete user')



    def __to_json_for_db(self):
        res = {
            "name": self.name,
            "email": self.email,
            "is_admin": self.is_admin,
            "password": self.__hashed_password
        }
        
        return res

    def to_json_for_user(self):
        res = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

        if self.is_admin:
            res["is_admin"] = self.is_admin
        
        return res

    @staticmethod
    def get_hashed_password(password):
        return generate_password_hash(password)

    def verify_hashed_password(self, password):
        return check_password_hash(self.__hashed_password, password)

    @staticmethod
    def get_user_by_id(user_id):
        user = User.get_user_by_id_if_exist(user_id)
        if user:
            return user
        else:
            raise BadRequestError('User Not Found')

    @staticmethod
    def get_user_by_id_if_exist(user_id):
        user = db_users.find_user_by_id(user_id)
        if user:
            return User(
                name=user.get('name'),
                email=user.get('email'),
                hashed_password=user.get('password'), 
                is_admin=user.get('is_admin', False),                
                id=str(user.get('_id'))
            )
        else:
            return False

    @staticmethod
    def get_user_by_email(email):
        user = User.get_user_by_email_if_exist(email)
        if user:
            return user
        else:
            raise BadRequestError('User with email {} Not Found'.format(escape(email)))

    @staticmethod
    def get_user_by_email_if_exist(email):
        user = db_users.find_user_by_email(email)
        if user:            
            return User(
                name=user.get('name'),
                email=user.get('email'),
                hashed_password=user.get('password'), 
                is_admin=user.get('is_admin', False),
                id=str(user.get('_id'))
            )
        else:
            return False
        
    