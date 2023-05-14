from flask import abort, Blueprint, jsonify, request
from controllers import userControllers
from controllers.functions import validateInputs

routes = Blueprint('routes', __name__)

@routes.route('/signUpUser', methods=["POST"])
def signUpUser():
    data = request.get_json()
    errors = []

    nameValidate = validateInputs.validateName(data.get('name'))
    if not nameValidate['status']:
        errors.append(nameValidate['mensagem'])
    
    emailValidate = validateInputs.validateEmail(data.get('email'))
    if not emailValidate['status']:
        errors.append(emailValidate['mensagem'])
    
    passwordValidate = validateInputs.validatePassword(data.get('password'))
    if not passwordValidate['status']:
        errors.append(passwordValidate['mensagem'])
    
    confirmPasswordValidation = validateInputs.validateConfirmPassword(data.get('password'), data.get('confirmPassword'))
    if not confirmPasswordValidation['status']:
        errors.append(confirmPasswordValidation['mensagem'])

    if errors:
        return jsonify({'mensagens': errors}), 400

    return userControllers.signUpUser(data)