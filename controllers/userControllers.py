from flask import jsonify, make_response, current_app
from bson import ObjectId

from models.db import db

import bcrypt
import jwt
import datetime

def signupUser(data):
    collection = db['usuarios']

    salt = bcrypt.gensalt(8)
    senha = data.get('senha')
    senhaHashed = bcrypt.hashpw(senha.encode('utf-8'), salt)

    if collection.count_documents({'email': data.get('email')}) == 0:
        collection.insert_one({
            'nome': data.get('nome'),
            'email': data.get('email'),
            'senha': senhaHashed
        })

        response = make_response(jsonify({'mensagem': 'Usuário criado com sucesso!'}), 201)
    else:
        response = make_response(jsonify({'mensagem': 'O e-mail fornecido já está cadastrado. Por favor, faça seu login!'}))
    
    return response

def loginUser(data):
    collection = db['usuarios']

    doesUserExists = collection.find_one({'email': data.get('email')})

    if doesUserExists is not None:
        dbPassword = doesUserExists['senha']

        if bcrypt.checkpw(data.get('senha').encode('utf-8'), dbPassword):
            payload = {
                'id': str(doesUserExists['_id']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }

            token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

            return jsonify({
                'userToken': token,
                'userData': {
                    '_id': doesUserExists['_id'],
                    'nome': doesUserExists['nome'],
                    'email': doesUserExists['email']
                },
                'mensagem': 'Usuário logado com sucesso!'
            }), 200
    else:
        return make_response(jsonify({'mensagem': 'Usuário não encontrado. Por favor, cadastre-se primeiramente.'}), 401)

def getUserData(id):
    collection = db['usuarios']

    doesUserExists = collection.find_one({'_id': ObjectId(id)})

    if doesUserExists is not None:
        return jsonify(doesUserExists)
    else:
        return make_response(jsonify({'mensagem': 'Usuário não encontrado.'}), 404)
    
def updateUserData(id, data):
    collection = db['usuarios']

    doesUserExists = collection.find_one({'_id': ObjectId(id)})

    # Lembre-se que é preciso verificar a senha, já que ela vem codificada do banco de dados
    # Não só aqui, na função de cima tbm

    if doesUserExists is not None:
        collection.update_one({'_id': ObjectId(id)}, {'$set': {'nome': data.get('nome'), 'email': data.get('email'), 'senha': data.get('senha')}})