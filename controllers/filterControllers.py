from flask import jsonify, make_response, current_app
from bson import ObjectId

from models.db import db

def getPositiveCases(id):
    collectionUser = db['usuarios']
    collectionCrattle = db['gados']

    doesUserExists = collectionUser.find_one({'_id': ObjectId(id)})

    if doesUserExists is not None:
        
        getHistoric = collectionCrattle.find({'idPecuarista': ObjectId(id)})
        # TODO: getHistoric['historico'] - Usar for in para percorrer o array de historicos
        # TODO: Pegar os bois que tem como dono aquele id + Pegar os historicos de cada boi retornado +
        # TODO: Pegar o mais recente e que seja positivo

    return