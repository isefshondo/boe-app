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
    
def getMenuData(id):
    collectionUser = db['usuarios']
    collectionBoi = db['gados']

    doesUserExist = collectionUser.find_one({'_id': ObjectId(id)})

    if doesUserExist is not None:
        nCasosRegistrados = collectionBoi.count_documents({'idPecuarista': id})
        boisCadastrados = collectionBoi.find({'idPecuarista': id})

        dataAtual = date.today()
        diferencaMinima = timedelta(days=365)

        gadosDoentes = 0

        if nCasosRegistrados == 0:
            return

        for dados in boisCadastrados:
            for historico in dados['historico']:
                if historico['resultado'] > 70:
                    diferenca = abs(historico['data'] - dataAtual)
                    if diferenca < diferencaMinima:
                        diferencaMinima = diferenca
                        gadosDoentes += 1

        calcCasosPositivos = (gadosDoentes * 100)/nCasosRegistrados

        return jsonify({
            'casosRegistrados': nCasosRegistrados,
            'casosPositivosAtualmente': calcCasosPositivos
        })
    else:
        return jsonify({'mensagem': 'Não foi possível encontrar este usuário'}), 401