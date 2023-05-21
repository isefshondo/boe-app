from flask import Blueprint, jsonify, request

from controllers import userControllers, filterControllers, OxControl
from controllers.functions import validateInputs, auth

routes = Blueprint('routes', __name__)

@routes.route('/cadastroUsuario', methods=["POST"])
def signUpUser():
    data = request.get_json()

    userData = {
        'name': data.get('nome'),
        'email': data.get('email'),
        'password': data.get('senha'),
        'confirmPassword': data.get('confirmaSenha')
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

    return userControllers.signupUser(data)

@routes.route('/loginUsuario', methods=["POST"])
def logInUser():
    data = request.get_json()

    loginUsuario = {
        'email': data.get('email'),
        'senha': data.get('senha')
    }

    return userControllers.loginUser(loginUsuario)

@routes.route('/perfilUsuario', methods=["GET"])
@auth.authenticationRequired
def getUserData(userToken):
    return userControllers.getUserData(userToken["id"])

@routes.route('/atualizarUsuario', methods=["POST"])
@auth.authenticationRequired
def updateUserData(userToken):
    data = request.get_json()

    errors = []

    nameValidate = validateInputs.validateName(data.get('nome'))
    if not nameValidate['status']:
        errors.append(nameValidate['mensagem'])
    
    emailValidate = validateInputs.validateEmail(data.get('email'))
    if not emailValidate['status']:
        errors.append(emailValidate['mensagem'])
    
    passwordValidate = validateInputs.validatePassword(data.get('senha'))
    if not passwordValidate['status']:
        errors.append(passwordValidate['mensagem'])

    if errors:
        return jsonify({'mensagens': errors}), 400

    return userControllers.updateUserData(userToken["id"], data)

@routes.route('/listarPositivos', methods=["GET"])
@auth.authenticationRequired
def getPositiveCases(userToken):
    return filterControllers.getPositiveCases(userToken['id'])

@routes.route('/listarGados', methods=["GET"])
@auth.authenticationRequired
def getAllCases(userToken):
    return filterControllers.getAllCases(userToken['id'])

# Here starts the Ox Controllers Part
@routes.route('/sendAnalyzeImage/<idGado>', methods=["POST"])
@auth.authenticationRequired
def sendImgToAnalyze(token, idGado):
    # In this route, I need to return the result and its details
    return OxControl.sendImgAnalyze(token['id'], idGado)

@routes.route('/signupOx', methods=["GET", "POST"])
@auth.authenticationRequired
def signupOx(token, data):
    oxData = {
        'numIdentificacao': data.get('codigo'),
        'oxName': data.get('nome'),
        'img': request.files['imagem']
    }
    return OxControl.signupOx(token['id'], oxData)

@routes.route('/updateOx/<idGado>', methods=["GET", "POST"])
@auth.authenticationRequired
def updateOx(idGado, data):
    if request.method == 'GET':
        return OxControl.getOxInfo(idGado)
    if request.method == 'POST':
        return OxControl.updateOx(idGado, data)