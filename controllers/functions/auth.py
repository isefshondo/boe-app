from flask import request, jsonify, current_app
from functools import wraps
from pymongo import MongoClient

import jwt

def doesUserExists(id):
    collection = db['user']
    userExists = collection.find_one({'id': id})

    return userExists is not None

def authRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization').split()[1]

        if token is None:
            return jsonify({'menssagem': 'Não foi fornecido um token de autenticação...'}), 401
        
        try:
            tokenAuth = jwt.decode(token, current_app.config['SECRET_KEY'])

            id = tokenAuth['id']

            if not doesUserExists(id):
                return jsonify({'menssagem': 'Usuário não encontrado...'}), 404
            
            return f(tokenAuth, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'menssagem': 'Tempo de uso atingido! Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'menssagem': 'Token inválido...'}), 401
        
    return decorated