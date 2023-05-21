from flask import current_app, jsonify, make_response, request
from bson import ObjectId

from models.db import db
from utils.cache import cache
from controllers.functions import gerarResultados

import datetime

def sendImgAnalyze(id):
    if "imagem" not in request.files:
        return jsonify({'mensagem': 'A imagem não foi enviada para a análise'}, 400)
    
    doesUserExist = (db['usuarios']).find_one({'_id': ObjectId(id)})

    if doesUserExist is None:
        return jsonify({'mensagem': 'Não foi possível encontrar um usuário com esta identificação'}, 400)
    
    img = request.files["imagem"]

    numBois = (db['gados']).count_documents({'idPecuarista': id})

    analysisResult = gerarResultados.generateResults()

    # TODO: Think of the returning data to fill the Phase and Next Symptons part

    dataReturned = {
        'img': img,
        'results': analysisResult
    }

    cache.set('tempData', dataReturned)

    # Maybe I will need to create a description

    return jsonify({
        'numIdGado': f"AI0{numBois}",
        'results': analysisResult
    })

def signupOx(id, data):
    doesUserExist = (db['usuarios']).find_one({'_id': ObjectId(id)})

    if doesUserExist is None:
        return jsonify({'mensagem': 'Não foi possível encontrar um usuário com esta identificação'}, 400)
    
    cachedInformation = cache.get('tempData')

    collectionOx = db['gados']

    recordsArray = []

    currentResults = {
        'results': cachedInformation['results'],
        'img': cachedInformation['img'],
        'date': datetime.datetime.now().date()

    }

    recordsArray.append(currentResults)

    collectionOx.insert_one({
        'numIdentificacao': data['numIdentificacao'],
        'nomeGado': data['oxName'],
        'fotoPerfil': data['img'],
        'status': 'Sem tratamento',
        'idPecuarista': id,
        'historico': recordsArray
    })

    cache.delete('tempData')

def getOxInfo(idOx):
    collectionOx = db['gados']

    getOx = collectionOx.find_one({'_id': ObjectId(idOx)})

    if getOx is None:
        return jsonify({'mensagem': 'Não foi possível encontrar o gado selecionado'}, 400)
    
    return jsonify({
        'numId': getOx['numIdentificacao'],
        'nomeGado': getOx['nomeGado'],
        'fotoPerfil': getOx['fotoPerfil'],
        'status': getOx['status'],
        'historico': getOx['historico']
    })

def updateOx(idOx, data):
    collectionOx = db['gados']

    getOx = collectionOx.find_one({'_id': ObjectId(idOx)})

    if getOx is None:
        return jsonify({'mensagem': 'Não foi possível encontrar o gado selecionado'}, 400)
    
    collectionOx.update_one({'_id': ObjectId(idOx)}, {'$set': {'status': data.get('status')}})