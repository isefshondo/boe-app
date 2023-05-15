from flask import jsonify, make_response, current_app, request

import jwt

def menu():
    auth = request.headers.get('Authorization')
    token = auth.split(' ')[1]

    if not auth:
        return jsonify({
            'mensagem': 'Seu login não foi autorizado...',
            'description': 'Não foi fornecido um token de autenticação'
        })
    
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])

        collection = db['gado']

        gadosRegistrados = len(collection.distinct('nId'))

    except jwt.ExpiredSignatureError:
        return jsonify({'mensagem': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'mensagem': 'Token inválido'}), 401

    return 