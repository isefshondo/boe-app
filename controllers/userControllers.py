from bson import ObjectId
from flask import jsonify, make_response, current_app
from models.db import db
from pymongo import errors

import bcrypt

collectionUser = db['usuarios']

def signupUser(name, email, password):
    collection = db['usuarios']

    salt = bcrypt.gensalt(8)
    senha = (password).encode('utf-8')
    senhaHashed = bcrypt.hashpw(senha, salt)

    try:
        if collection.count_documents({'email': email}) == 0:
            collection.insert_one({
                'nome': name,
                'email': email,
                'senha': senhaHashed
            })

            findUser = collection.find_one({'email': email})

            response = jsonify({
                'mensagem': 'Usuário criado com sucesso!',
                'idUsuario': str(findUser['_id']),
                'status': 200
            }), 200
        else:
            response = jsonify({
                'mensagem': 'O e-mail fornecido já está cadastrado. Por favor, faça seu login',
                'status': 400
            }), 400
            
        return response
    except Exception as err:
        return jsonify({'message': str(err)})

def loginUser(email, password):
    collection = db['usuarios']

    doesUserExist = collection.find_one({'email': email})

    if doesUserExist is not None:
        dbPassword = doesUserExist['senha']
        
        try:
            if bcrypt.checkpw((password).encode('utf-8'), dbPassword):
                response = jsonify({
                    'userData': {
                        'id': str(doesUserExist['_id']),
                        'nome': doesUserExist['nome'],
                        'email': doesUserExist['email']
                    },
                    'mensagem': 'Usuário logado com sucesso!',
                    'status': 200
                })
                response.status_code = 200

                return response
            else:
                response = jsonify({
                    'mensagem': 'E-mail ou senha incorretos...',
                    'status': 400
                }), 400
                return response
        except UnicodeDecodeError:
            response = jsonify({
                'mensagem': 'Erro ao decodificar a senha do usuário',
                'status': 500
            }), 500
            return response
    else:
        response = jsonify({
            'mensagem': 'Usuário não encontrado. Por favor, cadastre-se primeiramente.',
            'status': 404
        }), 404

        return response

def displayUserData(id):
    findUser = collectionUser.find_one({'_id': ObjectId(id)})

    if findUser is not None:
        try:
            return jsonify({
                'id': str(findUser['_id']),
                'name': findUser['nome'],
                'email': findUser['email'],
                'password': 'P4TTERN-PASS',
                'status': 200
            }), 200
        except Exception as err:
            return jsonify({
                'message': str(err),
                'status': 400
            }), 400
    else:
        response = jsonify({
            'message': 'Não foi possível encontrar o usuário...',
            'status': 404
        })
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
            
            response = jsonify({
                'message': 'Dados atualizados com sucesso',
                'status': 201
            })
            response.status_code = 201

            return response
        except errors.ConnectionFailure:
            return jsonify({
                'message': 'Conexão com base de dados falhou...',
                'description': 'Sinto muito! Houve uma falha em nossa base de dados.',
                'status': 500
            }), 500
        except errors.OperationFailure:
            return jsonify({
                'message': 'Operação do PyMongo falhou...',
                'description': 'Sinto muito! Não foi possível concluir a operação',
                'status': 500
            }), 500
    else:
        response = jsonify({
            'message': 'Não foi possível encontrar o usuário...',
            'status': 404
        })
        response.status_code = 404
        response.headers['Content-Type'] = 'application/json'

        return response
    
def deleteUser(id):
    findUser = collectionUser.find_one({'_id': ObjectId(id)})

    if findUser is not None:
        try:
            collectionUser.delete_one({'_id': ObjectId(id)})
        except errors.ConnectionFailure:
            return jsonify({
                'message': 'Conexão com base de dados falhou...',
                'description': 'Sinto muito! Houve uma falha em nossa base de dados.',
                'status': 500
            }), 500
        except errors.OperationFailure:
            return jsonify({
                'message': 'Operação do PyMongo falhou...',
                'description': 'Sinto muito! Não foi possível concluir a operação',
                'status': 500
            }), 500
    else:
        response = jsonify({
            'message': 'Não foi possível encontrar o usuário...',
            'status': 404
        })
        response.status_code = 404
        response.headers['Content-Type'] = 'application/json'
        
        return response