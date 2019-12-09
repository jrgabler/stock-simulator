from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

from controllers import UserController
from models import User

parser = reqparse.RequestParser()
parser.add_argument("username", help="This field cannot be blank", required=False)
parser.add_argument("password", help="This field cannot be blank", required=False)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        userController = UserController.UserController()

        if(userController.findByUsername(data["username"]) != None):
            return {"Message": f"User {data['username']} already exists"}

        try:
            userController.registration(data["username"], data["password"])
            access_token = create_access_token(identity = data["username"])
            refresh_token = create_refresh_token(identity = data["username"])

            return {
                "message": "User successfully created",
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        except:
            return {"message": "Something went wrong"}

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        userController = UserController.UserController()

        if(userController.findByUsername(data["username"]) == None):
            return {"message": f"User {data.username} doesn't exist"}

        if(userController.login(data["username"], data["password"])):
            access_token = create_access_token(identity = data["username"])
            refresh_token = create_refresh_token(identity = data["username"])

            return {
                "message": f"Logged in as {data['username']}",
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        else:
            return {"message": "Username or password is incorrect."}

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        return {"message": "User logout access"}

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):

        return {"message": "User logout refresh"}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        access_token = create_access_token(identity = user)
        return {"access_token": access_token}

class GetBalanceHistory(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        userController = UserController()

        user = userController.findByUsername(data["username"])
        history = userController.getUserBalanceHistory(user.getUserId)

        return history
