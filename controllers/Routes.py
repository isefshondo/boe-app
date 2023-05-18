from flask import Blueprint, jsonify, request

from controllers import userControllers, filterControllers, gadoControllers
from controllers.functions import validateInputs, auth, genResults

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

# Esta rota é apenas para mostrar o resultado dado pela análise na hora de cadastrar
# Na hora de subir a imagem
# TODO: Variáveis globais
@routes.route('/analisarResultados', methods=["POST"])
@auth.authenticationRequired
def cadastrarGado():
    guardarResultados = genResults.generateResults()
    return gadoControllers.analiseResultados(guardarResultados)