from bson import ObjectId
from flask import jsonify, make_response, current_app
from models.db import db
from pymongo import errors

import bcrypt
import jwt
import datetime

def signupUser(name, email, password):
    collection = db['usuarios']

    salt = bcrypt.gensalt(8)
    senha = (password).encode('utf-8')
    senhaHashed = bcrypt.hashpw(senha, salt)

    if collection.count_documents({'email': email}) == 0:
        collection.insert_one({
            'nome': name,
            'email': email,
            'senha': senhaHashed
        })

        response = make_response(jsonify({'mensagem': 'Usuário criado com sucesso!'}), 201)
    else:
        response = make_response(jsonify({'mensagem': 'O e-mail fornecido já está cadastrado. Por favor, faça seu login!'}))
    
    return response

def loginUser(email, password):
    collection = db['usuarios']

    doesUserExist = collection.find_one({'email': email})

    if doesUserExist is not None:
        dbPassword = doesUserExist['senha']
        
        try:
            if bcrypt.checkpw((password).encode('utf-8'), dbPassword):
                payload = {
                    'id': str(doesUserExist['_id']),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }

                token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

                return jsonify({
                    'userToken': token,
                    'userData': {
                        'id': str(doesUserExist['_id']),
                        'nome': doesUserExist['nome'],
                        'email': doesUserExist['email']
                    },
                    'mensagem': 'Usuário logado com sucesso!'
                }), 200
            else:
                return make_response(jsonify({'mensagem': 'Email ou senha incorretos...'}), 400)
        except UnicodeDecodeError:
            return make_response(jsonify({'mensagem': 'Erro ao decodificar a senha do usuário.'}), 500)
    else:
        return make_response(jsonify({'mensagem': 'Usuário não encontrado. Por favor, cadastre-se primeiramente.'}), 404)

def getUserData(id):
    collectionUser = db['usuarios']

    doesUserExist = collectionUser.find_one({'_id': ObjectId(id)})

    if doesUserExist is None:
        response = jsonify({'message': 'User not found...'})
        response.status_code = 404
        response.headers['Content-Type'] = 'application/json'

        return response
    
    return jsonify({
        'id': str(doesUserExist['_id']),
        'name': doesUserExist['nome'],
        'email': doesUserExist['email'],
        'password': 'PATTERN-PASS'
    }), 200
    
def updateUserData(id, name, email, password):
    collectionUser = db['usuarios']

    doesUserExist = collectionUser.find_one({'_id': ObjectId(id)})

    try:
        if password == 'PATTERN-PASS' or bcrypt.checkpw((password).encode('utf-8'), doesUserExist['senha']) is True:
            collectionUser.update_one({'_id': ObjectId(id)}, {'$set': {'nome': name, 'email': email}})
        else:
            salt = bcrypt.gensalt(8)
            senha = (password).encode('utf-8')
            pwHashed = bcrypt.hashpw(senha, salt)

            collectionUser.update_one({'_id': ObjectId(id)}, {'$set': {'nome': name, 'email': email, 'senha': pwHashed}})

            return jsonify({'message': 'Success! User data is updated'}), 201
    except errors.ConnectionFailure:
        return jsonify({
            'message': 'Sorry! An error ocurred in our database, we cant conclude operations right now',
            'description': 'Connection with database failed...'
        }), 500
    except errors.OperationFailure:
        return jsonify({
            'message': 'Sorry! We couldnt execute the process',
            'description': 'PyMongo operation failed'
        }), 500