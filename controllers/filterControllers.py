from flask import jsonify, make_response, current_app
from bson import ObjectId
from datetime import date, timedelta

from models.db import db

def getPositiveCases(id):
    collectionUser = db['usuarios']
    collectionCrattle = db['gados']

    doesUserExists = collectionUser.find_one({'_id': ObjectId(id)})

    boisFiltrados = []    
    dadosBois = None

    if doesUserExists is not None:
        
        getBois = collectionCrattle.find({'idPecuarista': ObjectId(id)})

        dataAtual = date.today()
        diferencaMinima = timedelta(days=365)

        for dados in getBois:
            for historico in dados['historico']:
                if historico['resultado'] > 70:
                    diferenca = abs(historico['data'] - dataAtual)
                    if diferenca < diferencaMinima:
                        diferencaMinima = diferenca
                        dadosBois = {
                            'nome': dados['nome'],
                            'fotoPerfil': dados['fotoPerfil'],
                            'status': dados['status'],
                            'resultados': historico
                        }
                        boisFiltrados.append(dadosBois)
        
        return boisFiltrados
    else:
        return jsonify({'mensagem': 'Não foi possível encontrar gados para este usuário.'}), 401