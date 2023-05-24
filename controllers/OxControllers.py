from controllers.utils.functions import GenResults
from flask import current_app, jsonify, make_response, request
from bson import ObjectId
from models.db import db
from controllers.utils import Cache

import datetime

def imageAnalyze(idUser, idOx, image):
    collectionUser = db['usuarios']
    collectionBoi = db['gados']

    doesUserExist = collectionUser.find_one({'_id': ObjectId(idUser)})

    genOxNumId = collectionBoi.count_documents({'idPecuarista': idUser})

    if doesUserExist is None:
        response = jsonify({'message': 'User not found...'})
        response.status_code = 404
        response.headers['Content-Type'] = 'application/json'

        return response
    
    sicknessResults = GenResults.genRandomResults()
    
    if image is not None:
        cachedResults = {
            'image': image,
            'results': sicknessResults,
            'date': datetime.datetime.now().date()
        }

        if idOx is None:
            Cache.cache.set('tempResults', cachedResults)

            return jsonify({
                'nTempIdOx': f"A0{genOxNumId + 1}",
                'results': {
                    'percentage': sicknessResults,
                    # Fase e complicacoes
                }
            })
        else:
            findOx = collectionBoi.find_one({'_id': ObjectId(idOx)})

            Cache.cache.set('tempResults', cachedResults)

            return jsonify({
                'nIdOx': findOx['numIdentificacao'],
                'nameOx': findOx['nomeGado'],
                'results': {
                    'percentage': sicknessResults,
                    # Fase e complicacoes
                }
            })
    else:
            return jsonify({'message': 'Error! There is no image to analyze'}), 404

def signupOx(id, idOx, tempId, name, pfp):
    collectionUser = db['usuarios']
    collectionBoi = db['gados']

    doesUserExist = collectionUser.find_one({'_id': ObjectId(id)})

    cachedResults = Cache.cache.get('tempResults')

    newRecords = None

    newRecord = {
        'imageAnalyzed': {
            'img': cachedResults['image'],
            'description': 'The lesion is circular with striking white borders.'
        },
        'results': cachedResults['results'],
        'date': cachedResults['date']
    }

    if idOx is not None:
        findOx = collectionBoi.find_one({'_id': ObjectId(idOx)})

        newRecords = findOx['historico']

        newRecords.append(newRecord)

        collectionBoi.update_one({'_id': idOx}, {'$set': {'historico': newRecords}})

        return jsonify({'message': 'Success! Data saved successfully'}), 201
    else:
        records = []

        records.append(newRecord)

        collectionBoi.insert_one({
            'numIdentificacao': tempId,
            'nomeGado': name,
            'fotoPerfil': pfp,
            'status': 'Sem tratamento',
            'idPecuarista': id,
            'historico': records
        })
    
    Cache.cache.delete('tempResults')

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