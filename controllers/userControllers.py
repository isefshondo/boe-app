from flask import jsonify, make_response

import bcrypt
import jwt
import datetime

def signUpUser(data):
    collection = db['users']

    saltComplexity = bcrypt.gensalt(8)
    password = data.get('password')
    hashPassword = bcrypt.hashpw(password.encode('utf-8'), saltComplexity)

    if db.collection.count_documents({'email': data.get('email')}) == 0:
        collection.insert_one({
            'name': data.get('name'),
            'email': data.get('email'),
            'password': hashPassword
        })

        response = make_response(jsonify({'mensagem': 'Usuário criado com sucesso!'}), 201)
    else:
        response = make_response(jsonify({'mensagem': 'O email usado já está cadastrado...'}), 400)
    
    return response

def logInUser(userData):
    collection = db['users']

    userLogin = db.collection.find_one({'email': userData['email']})

    if userLogin:
        loginPassword = userLogin['password']
        
        if bcrypt.checkpw(userData['password'], loginPassword.encode('utf-8')):
            return

    return make_response(jsonify({'mensagem': 'Não pode fazer o login! Tente novamente...'}), 401)