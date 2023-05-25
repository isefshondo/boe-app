from bson import ObjectId
from flask import current_app, jsonify, request
from functools import wraps

from models.db import db

import jwt

def RequireAuth(f):
    @wraps(f)

    def decorated(*args, **kwargs):
        collection = db["usuarios"]

        getToken = (request.headers["Authorization"]).split()[1]

        if getToken is None:
            response = jsonify({'message': 'No token provided in HTTP Request'})
            response.status_code = 400
            response.headers['Content-Type'] = 'application/json'

            return response
        
        try:
            decodedToken = jwt.decode(getToken, current_app.config["SECRET_KEY"], algorithms='HS256')

            doesUserExist = collection.find_one({'_id': ObjectId(decodedToken["id"])})

            if doesUserExist is None:
                response = jsonify({'message': 'User wasnt found by the server'})
                response.status_code = 500
                response.headers['Content-Type'] = 'application/json'
                
                return response
            
            return f(decodedToken, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            response = jsonify({'message': 'Reached Timeout'})
            response.status_code = 500
            return response
        except jwt.InvalidTokenError:
            response = jsonify({'message': 'Invalid Token'})
            response.status_code = 400
            return response
    return decorated