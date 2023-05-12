from flask import Blueprint
from controllers import UsersControllers

routes = Blueprint("routes", __name__)

@routes.route("/signupUser", methods=["POST"])
def signUpUser():
    return UsersControllers.createUser()

@routes.route("/signinUser", methods=["POST"])
def signInUser():
    return

@routes.route("/registerCrattle", methods=["POST"])
def registerCrattle():
    return