from flask import jsonify, make_response, current_app, request
from bson import ObjectId

from models.db import db
from controllers.functions import gerarResultados

def analiseImagem():
    global guardaResultado

    if "imagem" not in request.files:
        return jsonify({'mensagem': 'Não há imagem...'}, 400)

    # Imagem é o nome do campo onde deve ser enviado o valor da imagem (a imagem em si)
    img = request.files['imagem']
    
    img.save('controllers/temp/' + img.filename)

    guardaResultado = gerarResultados.generateResults()
    
    descricaoFaseContaminacao = None
    descricaoComplicacao = None

    if guardaResultado <= 50:
        descricaoFaseContaminacao = 'O animal pode estar no estágio de colonização, na qual a pele aparenta uma aparência seca, escamosa e avermelhada.'
        descricaoComplicacao = 'Irritação e inflamação da pele, o que causa coceira. Outra complicação seria a pele ficar mais suscetiva a infecções secundárias bacterianas, levando a complicações adicionais.'
    if guardaResultado > 50:
        descricaoFaseContaminacao = 'O animal pode estar no estágio de lesões primárias, na qual há a perda de pelos e a pele do animal apresenta crosta e escamas, podendo estar inflamada e dolorida'
        descricaoComplicacao = 'Dificulta o movimento do animal e afeta a produção e a qualidade do leite em vacas leiteiras'

    return jsonify({
        'resultadoAnalise': guardaResultado,
        'faseContaminacao': descricaoFaseContaminacao,
        'complicacoes': descricaoComplicacao
    })