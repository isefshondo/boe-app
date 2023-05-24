from flask import jsonify, make_response, current_app
from bson import ObjectId
from datetime import date, timedelta

from models.db import db

def getPositiveCases(id):
    collectionUser = db['usuarios']
    collectionBoi = db['gados']

    doesUserExist = collectionUser.find_one({'_id': ObjectId(id)})

    boisFiltrados = []
    dadosBoi = None
    historicoBoi = None

    if doesUserExist is not None:
        
        getBois = collectionBoi.find({'idPecuarista': id})

        dataAtual = date.today()
        diferencaMinima = timedelta(days=365)

        for dados in getBois:
            for historico in dados['historico']:
                if historico['resultado'] > 70:
                    diferenca = abs(historico['data'] - dataAtual)
                    if diferenca < diferencaMinima:
                        diferencaMinima = diferenca
                        historicoBoi = historico
            
            dadosBoi = {
                'id': dados['_id'],
                'nome': dados['nome'],
                'fotoPerfil': dados['fotoPerfil'],
                'status': dados['status'],
                'historicoRecente': historicoBoi
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
    historicoBoi = None

    if doesUserExist is not None:
        
        getBois = collectionBoi.find({'idPecuarista': id})

        dataAtual = date.today()
        diferencaMinima = timedelta(days=365)

        for dados in getBois:
            for historico in dados['historico']:
                diferenca = abs(historico['data'] - dataAtual)
                if diferenca < diferencaMinima:
                    diferencaMinima = diferenca
                    historicoBoi = historico
            
            dadosBoi = {
                'id': dados['_id'],
                'nome': dados['nome'],
                'fotoPerfil': dados['fotoPerfil'],
                'status': dados['status'],
                'historicoRecente': historicoBoi
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
        return None
    
    animalsRegistered = collectionBoi.find({'idPecuarista': idUser})

    currentDate = date.today()
    minDifference = timedelta(days=365)

    sickAnimals = 0
    healthyAnimals = 0

    for dados in animalsRegistered:
        for historico in dados['historico']:
            difference = abs(historico['data'] - currentDate)
            if historico['resultado'] > 75:
                if difference < minDifference:
                    minDifference = difference
                    sickAnimals += 1
            else:
                if difference < minDifference:
                    minDifference = difference
                    healthyAnimals += 1
    
    positiveCases = (sickAnimals * 100)/numRegisteredCases

    return jsonify({
        'userName': doesUserExist['nome'],
        'registeredCases': numRegisteredCases,
        'positiveCases': positiveCases,
        'generalCases': {
            'positive': sickAnimals,
            'negative': healthyAnimals
        }
    })