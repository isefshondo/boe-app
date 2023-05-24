from controllers import FilterControllers, OxControllers, UserControllers
from controllers.utils.functions import ValInputs
from controllers.utils.security import Authentication
from flask import Blueprint, jsonify, request

routes = Blueprint('routes', __name__)

@routes.route('/signupUser', methods=["POST"])
def signUpUser():
    data = request.get_json()

    userData = {
        'name': data.get('name'),
        'email': data.get('email'),
        'password': data.get('password'),
        'confirmPassword': data.get('confirmPassword')
    }

    errors = []

    nameValidate = ValInputs.validateName(userData['name'])
    if not nameValidate['status']:
        errors.append(nameValidate['mensagem'])
    
    emailValidate = ValInputs.validateEmail(userData['email'])
    if not emailValidate['status']:
        errors.append(emailValidate['mensagem'])
    
    passwordValidate = ValInputs.validatePassword(userData['password'])
    if not passwordValidate['status']:
        errors.append(passwordValidate['mensagem'])
    
    confirmPasswordValidation = ValInputs.validateConfirmPassword(userData['password'], userData['confirmPassword'])
    if not confirmPasswordValidation['status']:
        errors.append(confirmPasswordValidation['mensagem'])

    if errors:
        return jsonify({'mensagens': errors}), 400

    return UserControllers.signupUser(userData['name'], userData['email'], userData['password'])

@routes.route('/loginUser', methods=["POST"])
def logInUser():
    data = request.get_json()

    loginUsuario = {
        'email': data.get('email'),
        'senha': data.get('password')
    }

    return UserControllers.loginUser(loginUsuario['email'], loginUsuario['senha'])

@routes.route('/atualizarUsuario', methods=["GET", "POST"])
@Authentication.RequireAuth
def updateUserData(userToken):
    data = request.get_json()

    userData = {
        'name': data.get('name'),
        'email': data.get('email'),
        'password': data.get('password')
    }

    if request.method == "GET":
        return UserControllers.getUserData(userToken["id"])
    
    if request.method == "POST":
        errors = []

        nameValidate = ValInputs.validateName(userData['name'])
        if not nameValidate['status']:
            errors.append(nameValidate['mensagem'])
        
        emailValidate = ValInputs.validateEmail(userData['email'])
        if not emailValidate['status']:
            errors.append(emailValidate['mensagem'])
        
        passwordValidate = ValInputs.validatePassword(userData['password'])
        if not passwordValidate['status']:
            errors.append(passwordValidate['mensagem'])

        if errors:
            return jsonify({'mensagens': errors}), 400

        return UserControllers.updateUserData(userToken["id"], userData['name'], userData['email'], userData['password'])

@routes.route('/listarPositivos', methods=["GET"])
@Authentication.RequireAuth
def getPositiveCases(userToken):
    return FilterControllers.getPositiveCases(userToken['id'])

@routes.route('/listarGados', methods=["GET"])
@Authentication.RequireAuth
def getAllCases(userToken):
    return FilterControllers.getAllCases(userToken['id'])

@routes.route('/menu', methods=["GET"])
@Authentication.RequireAuth
def getMenuData(userToken):
    return FilterControllers.getMenuData(userToken['id'])

# Here starts the Ox Controllers Part
@routes.route('/imageAnalyze/<idOx>', methods=["POST"])
@Authentication.RequireAuth
def sendImgToAnalyze(token, idOx):
    file = request.files['file']
    # In this route, I need to return the result and its details
    return OxControllers.imageAnalyze(token['id'], idOx, file)

@routes.route('/signupOx/<idOx>', methods=["POST"])
@Authentication.RequireAuth
def signupOx(token, idOx):
    data = request.get_json()

    oxData = {
        'nTempIdOx': data.get('id'),
        'name': data.get('name'),
        'pfp': request.files['file']
    }

    return OxControllers.signupOx(token['id'], idOx, oxData['nTempIdOx'], oxData['name'], oxData['pfp'])

@routes.route('/updateOx/<idGado>', methods=["GET", "POST"])
@Authentication.RequireAuth
def updateOx(idGado, data):
    if request.method == 'GET':
        return OxControllers.getOxInfo(idGado)
    if request.method == 'POST':
        return OxControllers.updateOx(idGado, data)