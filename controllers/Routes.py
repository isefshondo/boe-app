from flask import Blueprint, jsonify, request
from controllers import userControllers, appControllers
from controllers.functions import validateInputs

routes = Blueprint('routes', __name__)

@routes.route('/signUpUser', methods=["POST"])
def signUpUser():
    data = request.get_json()

    userData = {
        'name': data.get('name'),
        'email': data.get('email'),
        'password': data.get('password'),
        'confirmPassword': data.get('confirmPassword')
    }

    errors = []

    nameValidate = validateInputs.validateName(userData['name'])
    if not nameValidate['status']:
        errors.append(nameValidate['mensagem'])
    
    emailValidate = validateInputs.validateEmail(userData['email'])
    if not emailValidate['status']:
        errors.append(emailValidate['mensagem'])
    
    passwordValidate = validateInputs.validatePassword(userData['password'])
    if not passwordValidate['status']:
        errors.append(passwordValidate['mensagem'])
    
    confirmPasswordValidation = validateInputs.validateConfirmPassword(userData['password'], userData['confirmPassword'])
    if not confirmPasswordValidation['status']:
        errors.append(confirmPasswordValidation['mensagem'])

    if errors:
        return jsonify({'mensagens': errors}), 400

    return userControllers.signUpUser(data)

@routes.route('/logInUser', methods=["POST"])
def logInUser():
    data = request.get_json()

    userLogin = {
        'email': data.get('email'),
        'password': data.get('password').encode('utf-8')
    }

    return userControllers.logInUser(userLogin)

# @routes.route('/perfilUsuario/<id>', methods=["GET"])
# def userProfile(id):
