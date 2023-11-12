from bson import ObjectId
from flask import jsonify
from models.db import db

import base64

def getPositiveCases(id):
    collectionUser = db['usuarios']
    collectionBoi = db['gados']

    doesUserExist = collectionUser.find_one({'_id': ObjectId(id)})

    boisFiltrados = []
    dadosBoi = None

    if doesUserExist is not None:

        getBois = collectionBoi.find({
            '$and': [
                {'idPecuarista': id},
                {'historico': {'$exists': True}}
            ]
        })

        for dados in getBois:

            if dados['historico'][len(dados['historico']) - 1]['results'] > 50:            
                dadosBoi = {
                    'id': str(dados['_id']),
                    'tempId': dados['numIdentificacao'],
                    'nome': dados['nomeGado'],
                    'fotoPerfil': base64.b64encode(dados['fotoPerfil']).decode('utf-8'),
                    'status': dados['status'],
                    'historicoBoi': dados['historico'][len(dados['historico']) - 1]['results']
                }
            else:
                dadosBoi = {
                    'id': str(dados['_id']),
                    'tempId': dados['numIdentificacao'],
                    'nome': dados['nomeGado'],
                    'fotoPerfil': base64.b64encode(dados['fotoPerfil']).decode('utf-8'),
                    'status': dados['status'],
                    'historicoBoi': None
                }

            boisFiltrados.append(dadosBoi)
        
        return jsonify({'filtroBois': boisFiltrados})
    else:
        return jsonify({'mensagem': 'Não foi possível encontrar gados para este usuário.'}), 401

def getAllCases(id):
    collectionUser = db['usuarios']
    collectionBoi = db['gados']

    doesUserExist = collectionUser.find_one({'_id': ObjectId(id)})

    boisFiltrados = []
    dadosBoi = None

    if doesUserExist is not None:
        
        getBois = collectionBoi.find({
            '$and': [
                {'idPecuarista': id},
                {'historico': {'$exists': True}}
            ]
        })

        for dados in getBois:
            fotoPerfil = base64.b64encode(dados['fotoPerfil']).decode('utf-8')
            
            dadosBoi = {
                'id': str(dados['_id']),
                'tempId': dados['numIdentificacao'],
                'nome': dados['nomeGado'],
                'fotoPerfil': fotoPerfil,
                'status': dados['status'],
                'historicoRecente': dados['historico'][len(dados['historico']) - 1]['results']
            }

            boisFiltrados.append(dadosBoi)
        
        return jsonify({'filtroTodos': boisFiltrados})
    else:
        return jsonify({'mensagem': 'Não foi possível encontrar gados para este usuário.'}), 401

def getMenuData(idUser):
    collectionUser = db['usuarios']
    collectionBoi = db['gados']

    doesUserExist = collectionUser.find_one({'_id': ObjectId(idUser)})

    if doesUserExist is None:
        response = jsonify({'message': 'User not found...'})
        response.status_code = 404
        response.headers['Content-Type'] = 'application/json'

        return response

    numRegisteredCases = collectionBoi.count_documents({'idPecuarista': idUser})

    if numRegisteredCases == 0:
        return jsonify({
            'userName': doesUserExist['nome'],
            'registeredCases': 0,
            'positiveCases': 0,
            'generalCases': {
                'positive': 0,
                'negative': 0
            }
        })

    countAnimalsId = collectionBoi.count_documents({'idPecuarista': idUser})

    countAnimalsPositive = collectionBoi.count_documents({
        '$and': [
            {'idPecuarista': idUser},
            {'historico.results': {'$gt': 50}}
        ]
    })

    positiveCases = (countAnimalsPositive * 100)/countAnimalsId

    return jsonify({
        'userName': doesUserExist['nome'],
        'registeredCases': countAnimalsId,
        'positiveCases': round(positiveCases)
    })