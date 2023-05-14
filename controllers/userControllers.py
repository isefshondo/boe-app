from flask import jsonify

import bcrypt

def signUpUser(data):
    salt = bcrypt.gensalt(8)
    password = data.get('password')
    hash = bcrypt.hashpw(password, salt)

    collection = ['users']

    # Criar condição para verificar se o email ainda não existe

    collection.insert_one({
        'name': data.get('name'),
        'email': data.get('email'),
        'password': hash
    })

    return jsonify({'mensagem': 'Usuário criado com sucesso!'})