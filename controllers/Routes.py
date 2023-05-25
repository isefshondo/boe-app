from controllers import filterControllers, OxControllers, userControllers
from controllers.utils.functions import ValInputs
from controllers.utils.security import Authentication
from flask import Blueprint, jsonify, request
from PIL import Image

import base64
import io

routes = Blueprint('routes', __name__)

@routes.route('/signupUser', methods=["POST"])
def signUpUser():
    data = request.get_json()

    userData = {
        'name': data.get('name'),
        'email': data.get('email'),
        'password': data.get('password')
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

    if errors:
        return jsonify({'mensagens': errors}), 400

    return userControllers.signupUser(userData['name'], userData['email'], userData['password'])

@routes.route('/loginUser', methods=["POST"])
def logInUser():
    data = request.get_json()

    loginUsuario = {
        'email': data.get('email'),
        'senha': data.get('password')
    }

    return userControllers.loginUser(loginUsuario['email'], loginUsuario['senha'])

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
        return userControllers.getUserData(userToken["id"])
    
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

        return userControllers.updateUserData(userToken["id"], userData['name'], userData['email'], userData['password'])

@routes.route('/listarPositivos', methods=["GET"])
@Authentication.RequireAuth
def getPositiveCases(userToken):
    return filterControllers.getPositiveCases(userToken['id'])

@routes.route('/listarGados', methods=["GET"])
@Authentication.RequireAuth
def getAllCases(userToken):
    return filterControllers.getAllCases(userToken['id'])

@routes.route('/menu', methods=["GET"])
@Authentication.RequireAuth
def getMenuData(userToken):
    return filterControllers.getMenuData(userToken['id'])

# Here starts the Ox Controllers Part
@routes.route('/imageAnalyze/', methods=["POST"])
@Authentication.RequireAuth
def sendImgToAnalyze(token):
    data = request.get_json()

    fileReceived = data['file']

    imgDecoded = base64.b64decode(fileReceived)

    image = Image.open(io.BytesIO(imgDecoded))

    return OxControllers.imageAnalyze(token['id'], None, image)

@routes.route('/imageAnalyze/<idOx>', methods=["POST"])
@Authentication.RequireAuth
def analyzeRegisteredOx(token, idOx):
    data = request.get_json()

    fileReceived = data['file']

    imgDecoded = base64.b64decode(fileReceived)

    image = Image.open(io.BytesIO(imgDecoded))

    return OxControllers.imageAnalyze(token['id'], idOx, image)

@routes.route('/signupOx', methods=["POST"])
@Authentication.RequireAuth
def signupOx(token):
    data = request.form

    image = request.files.get('image')

    oxData = {
        'nTempIdOx': data.get("nTempIdOx"),
        'name': data.get("name"),
        'file': image
    }

    return OxControllers.signupOx(token['id'], None, oxData['nTempIdOx'], oxData['name'], oxData['file'])

@routes.route('/signupOx/<idOx>', methods=["POST"])
@Authentication.RequireAuth
def updateRegisteredOx(token, idOx):
    data = request.get_json()

    fileReceived = data['file']

    imgDecoded = base64.b64decode(fileReceived)

    image = Image.open(io.BytesIO(imgDecoded))

    oxData = {
        'nTempIdOx': data.get("nTempIdOx"),
        'name': data.get("name"),
        'file': image
    }

    return OxControllers.signupOx(token['id'], idOx, oxData['nTempIdOx'], oxData['name'], oxData['file'])

@routes.route('/updateOx/<idGado>', methods=["GET", "POST"])
@Authentication.RequireAuth
def updateOx(idGado, data):
    if request.method == 'GET':
        return OxControllers.getOxInfo(idGado)
    if request.method == 'POST':
        return OxControllers.updateOx(idGado, data)