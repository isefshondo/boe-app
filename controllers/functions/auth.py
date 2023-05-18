from flask import current_app, jsonify, request
from functools import wraps
from bson import ObjectId

from models.db import db

import jwt

def authenticationRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        collection = db['usuarios']

        token = (request.headers['Authorization']).split()[1]

        if token is None:
            return jsonify({'mensagem': 'Forneça um token de autenticação para continuar com a operação...'}), 401
        
        try:
            decodedToken = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')

            doesUserExists = collection.find_one({'_id': ObjectId(decodedToken['id'])})

            if doesUserExists is None:
                return jsonify({'mensagem': 'Usuário não foi encontrado...'}), 404
            
            return f(decodedToken, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'mensagem': 'Tempo de uso atingido! Faça novamente o login para explorar o aplicativo'}), 404
        except jwt.InvalidTokenError:
            return jsonify({'mensagem': 'Ação não é válida (Token inválido).'}), 401
        
    return decorated