from flask import jsonify, make_response, current_app
from bson import ObjectId

def analiseResultados(resultado):
    if resultado > 50:
        return
    elif resultado == 50:
        return
    elif resultado < 50:
        return