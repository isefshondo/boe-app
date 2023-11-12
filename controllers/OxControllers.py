from flask import Flask, jsonify
from bson import ObjectId, Binary
from PIL import Image

import datetime
import base64
import numpy as np
import cv2
import io

from controllers.utils.functions import GenResults
from controllers.utils import Cache

from models.db import db

collectionUser = db['usuarios']
collectionBoi = db['gados']

def getResults(idUser, idOx):
    findUser = collectionUser.find_one({'_id': ObjectId(idUser)})
    countOx = collectionBoi.count_documents({'idPecuarista': idUser})

    if findUser is not None:
        try:
            results = GenResults.genRandomResults()

            tempIdOx = f'A{countOx + 1}'

            saveResults = {
                'nTempIdOx': tempIdOx,
                'result': results['results'],
                'date': datetime.datetime.now().date().isoformat()
            }

            Cache.cache.set('tempData', saveResults)

            if idOx is None:
                collectionBoi.insert_one({
                    'numIdentificacao': tempIdOx,
                    'idPecuarista': idUser
                })

                return {
                    'nTempIdOx': tempIdOx,
                    'results': {
                        'percentage': results['results'],
                        'phase': results['currentPhase'],
                        'nextSymptons': results['symptonsPhase'],
                        'level': results['level'],
                        'details': results['details']
                    },
                    'status': 201
                }
            else:
                findOx = collectionBoi.find_one({'_id': ObjectId(idOx)})

                return {
                    'nIdOx': findOx['numIdentificacao'],
                    'nameOx': findOx['nomeGado'],
                    'results': {
                        'percentage': results['results'],
                        'phase': results['currentPhase'],
                        'nextSymptons': results['symptonsPhase']
                    },
                    'status': 201
                }
        except Exception as err:
            return {'message': str(err)}
    else:
        response = jsonify({
            'message': 'Não foi possível encontrar o usuário...',
            'status': 201
        })
        response.status_code = 404
        response.headers['Content-Type'] = 'application/json'

        return response

def signupCow(idUser, idCow, image, name):

    tempData = Cache.cache.get('tempData')

    print(tempData)

    newRecords = None

    newRecord = {
        'imageAnalyzed': {
            'description': 'Apresenta lesões circulares com bordar esbranquiçadas.'
        },
        'results': tempData['result'],
        'date': tempData['date']
    }

    try:
        if idCow is None and image is not None:
            records = []

            records.append(newRecord)

            imgBytes = image.read()

            collectionBoi.update_one(
                {
                    '$and': [
                        {'idPecuarista': idUser},
                        {'numIdentificacao': tempData['nTempIdOx']}
                    ]
                },
                {'$set': {
                    'nomeGado': name,
                    'fotoPerfil': Binary(imgBytes),
                    'status': 'Sem tratamento',
                    'historico': records
                }}
            )
        else:
            findOx = collectionBoi.find_one({'_id': ObjectId(idCow)})

            newRecords = findOx['historico']

            newRecords.append(newRecord)

            collectionBoi.update_one({'_id': ObjectId(idCow)}, {'$set': {'historico': newRecords}})

        Cache.cache.delete('tempData')
        return jsonify({
            'message': 'Success! Data saved successfully',
            'status': 201
        }), 201
    except Exception as err:
        return jsonify({'message': str(err)})
        
def getCow():
    tempData = Cache.cache.get('tempData')

    try:
        return jsonify({
            'tempIdCow': tempData['nTempIdOx'],
            'results': tempData['result'],
            'date': tempData['date'],
            'status': 200
        }), 200
    except Exception as err:
        return jsonify({'message': str(err)})

def getOxInfo(idOx):
    collectionOx = db['gados']

    getOx = collectionOx.find_one({'_id': ObjectId(idOx)})

    if getOx is None:
        return jsonify({
            'mensagem': 'Não foi possível encontrar o gado selecionado',
            'status': 400
        }), 400
    
    return jsonify({
        'cowData': {
            'numId': getOx['numIdentificacao'],
            'nomeGado': getOx['nomeGado'],
            'fotoPerfil': getOx['fotoPerfil'],
            'status': getOx['status'],
            'historico': getOx['historico']
        },
        'status': 200
    }), 200

def updateOx(idOx, data):
    collectionOx = db['gados']

    getOx = collectionOx.find_one({'_id': ObjectId(idOx)})

    if getOx is None:
        return jsonify({'mensagem': 'Não foi possível encontrar o gado selecionado'}, 400)
    
    collectionOx.update_one({'_id': ObjectId(idOx)}, {'$set': {'status': data.get('status')}})

def rotateImage(img):
    imgBytes = base64.b64decode(img.split(",")[-1])

    imgPil = Image.open(io.BytesIO(imgBytes))

    image = np.array(imgPil)

    height, width = image.shape[0], image.shape[1]

    matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 180, 1.0)

    imgRotated = cv2.warpAffine(image, matrix, (width, height))

    rgb = cv2.cvtColor(imgRotated, cv2.COLOR_BGR2RGB)

    _, imgBase64 = cv2.imencode("." + imgPil.format.lower(), rgb)

    imgBase64 = "data:image/" + imgPil.format.lower() + ";base64," + base64.b64encode(imgBase64).decode('utf-8')

    return imgBase64