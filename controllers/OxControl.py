from flask import current_app, jsonify, make_response, request

from models.db import db
from utils.cache import cache
from controllers.functions import gerarResultados

def sendImgAnalyze():
    if "imagem" not in request.files:
        return jsonify({'mensagem': 'A imagem não foi enviada para a análise'}, 400)
    
    img = request.files["imagem"]

    analysisResult = gerarResultados.generateResults()

    # TODO: Think of the returning data to fill the Phase and Next Symptons part

    dataReturned = {
        'img': img,
        'results': analysisResult
    }

    cache.set('tempData', dataReturned)

    return jsonify({
        'results': analysisResult
    })