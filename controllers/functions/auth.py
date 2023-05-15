from flask import request, jsonify
from functools import wraps
from pymongo import MongoClient

import jwt

def doesUserExists(id):
    collection = db['user']
    userExists = collection.find_one({'id': id})

    return userExists is not None