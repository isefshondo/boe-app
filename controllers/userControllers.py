from bson import ObjectId
from flask import jsonify, make_response, current_app
from models.db import db
from pymongo import errors

import bcrypt
import jwt
import datetime

collectionUser = db['usuarios']

def signupUser(name, email, password):
    salt = bcrypt.gensalt(8)
    senha = (password).encode('utf-8')
    senhaHashed = bcrypt.hashpw(senha, salt)

    try:
        if collectionUser.count_documents({'email': email}) == 0:
            collectionUser.insert_one({
                'nome': name,
                'email': email,
                'senha': senhaHashed
            })

            response = make_response(jsonify({'mensagem': 'Usuário criado com sucesso!'}), 201)
        else:
            response = make_response(jsonify({'mensagem': 'O e-mail fornecido já está cadastrado. Por favor, faça seu login!'}))
        
        return response
    except Exception as err:
        return jsonify({'message': str(err)})

def loginUser(email, password):
    doesUserExist = collectionUser.find_one({'email': email})

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
                raise ValueError('Email ou senha incorretos...')
        except UnicodeDecodeError:
            return make_response(jsonify({'mensagem': 'Erro ao decodificar a senha do usuário.'}), 500)
    else:
        raise ValueError('Usuário não encontrado. Por favor, cadastre-se primeiramente.')

def displayUserData(id):
    findUser = collectionUser.find_one({'_id': ObjectId(id)})

    if findUser is not None:
        try:
            return jsonify({
                'id': str(findUser['_id']),
                'name': findUser['nome'],
                'email': findUser['email'],
                'password': 'P4TTERN-PASS'
            }), 200
        except Exception as err:
            return jsonify({'message': str(err)})
    else:
        response = jsonify({'message': 'Não foi possível encontrar o usuário...'})
        response.status_code = 404
        response.headers['Content-Type'] = 'application/json'

        return response

def updateUser(id, name, email, password):
    findUser = collectionUser.find_one({'_id': ObjectId(id)})

    if findUser is not None:
        try:
            if password == 'P4TTERN-PASS' or bcrypt.checkpw((password).encode('utf-8'), findUser['senha']) is True:
                collectionUser.update_one({'_id': ObjectId(id)}, {'$set': {'nome': name, 'email': email}})
            else:
                salt = bcrypt.gensalt(8)
                pw = (password).encode('utf-8')
                pwHashed = bcrypt.hashpw(pw, salt)

                collectionUser.update_one({'_id': ObjectId(id)}, {'$set': {'nome': name, 'email': email, 'senha': pwHashed}})
            
            response = jsonify({'message': 'Dados atualizados com sucesso'})
            response.status_code = 201

            return response
        except errors.ConnectionFailure:
            return jsonify({
                'message': 'Conexão com base de dados falhou...',
                'description': 'Sinto muito! Houve uma falha em nossa base de dados.'
            }), 500
        except errors.OperationFailure:
            return jsonify({
                'message': 'Operação do PyMongo falhou...',
                'description': 'Sinto muito! Não foi possível concluir a operação'
            })
    else:
        response = jsonify({'message': 'Não foi possível encontrar o usuário...'})
        response.status_code = 404
        response.headers['Content-Type'] = 'application/json'

        return response