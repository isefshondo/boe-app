from flask import jsonify, make_response, current_app
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
            })
    else:
        return make_response(jsonify({'mensagem': 'Usuário não encontrado. Por favor, cadastre-se primeiramente.'}), 401)

def getUserData(data):
    return 