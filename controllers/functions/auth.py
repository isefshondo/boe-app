from flask import current_app, jsonify, request
from functools import wraps

from models.db import db

import jwt

def authenticationRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization']
        return jsonify({'mensagem': token})

# def doesUserExists(id):
#     collection = db['user']
#     userExists = collection.find_one({'_id': id})

#     print

#     return userExists is not None

# def authRequired(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.headers['Authorization'].split()[1]

#         if token is None:
#             return jsonify({'message': 'Não foi fornecido um token de autenticação...'}), 401
        
#         try:
#             tokenAuth = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

#             id = tokenAuth['id']

#             if not doesUserExists(id):
#                 return jsonify({'message': 'Usuário não encontrado...'}), 404
            
#             return f(tokenAuth, *args, **kwargs)
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': 'Tempo de uso atingido! Token expirado'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'message': 'Token inválido...'}), 401
        
#     return decorated