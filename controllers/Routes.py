from controllers import filterControllers, OxControllers, userControllers
from controllers.utils.functions import ValInputs
from flask import Blueprint, jsonify, request, json

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

@routes.route('/updateUser/<id>', methods=['GET', 'PUT'])
def updateUser(id):
    if request.method == 'GET':
        return userControllers.displayUserData(id)
    if request.method == 'PUT':
        data = request.get_json()

        userData = {
            'name': data.get('name'),
            'email': data.get('email'),
            'password': data.get('password')
        }

        return userControllers.updateUser(id, userData['name'], userData['email'], userData['password'])
    
@routes.route('/deleteUser/<id>', methods=['DELETE'])
def deletarUsuario(id):
    return userControllers.deleteUser(id)

@routes.route('/listarPositivos/<idUser>', methods=["GET"])
def getPositiveCases(idUser):
    return filterControllers.getPositiveCases(idUser)

@routes.route('/listarGados/<idUser>', methods=["GET"])
def getAllCases(idUser):
    return filterControllers.getAllCases(idUser)

@routes.route('/menu/<idUser>', methods=["GET"])
def getMenuData(idUser):
    return filterControllers.getMenuData(idUser)

@routes.route('/getResults/<idUser>', methods=["GET"])
def getResults(idUser):
    return OxControllers.getResults(idUser, None)

@routes.route('/getResults/<idUser>/<idOx>', methods=["GET"])
def getUpdatedResults(idUser, idOx):
    return OxControllers.getResults(idUser, idOx)

@routes.route('/signupCow/<idUser>', methods=['GET', 'POST'])
def signupCow(idUser):
    if request.method == 'GET':
        return OxControllers.getCow()
    if request.method == 'POST':

        cowData = {
            'nameCow': request.form['cowName'],
            'image': request.files['picInput']
        }

        return OxControllers.signupCow(idUser, None, cowData['image'], cowData['nameCow'])

@routes.route('/signupCow/<idUser>/<idCow>', methods=['GET', 'POST'])
def signupExistingCow(idUser, idCow):
    if request.method == 'GET':
        return OxControllers.getCow()
    if request.method == 'POST':

        cowData = {
            'nTempId': request.form['tempIdCow'],
            'nameCow': request.form['name'],
            'image': request.files['image']
        }

        return OxControllers.signupCow(idUser, idCow, cowData['image'], cowData['nTempId'], cowData['nameCow'])
    
@routes.route('/rotateImage', methods=['POST'])
def rotateImage():
    data = request.json

    imgBase = data['image']

    rotatedImage = OxControllers.rotateImage(imgBase)

    return jsonify({
        'message': 'Imagem rotacionada',
        'imgRotacionada': rotatedImage,
        'status': 201
    })