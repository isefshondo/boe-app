from flask import request, redirect, jsonify, abort
from functions import ValidateForm as validateInputs

def createUser():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')

    validateInputs.validateForm(name, email, password, confirmPassword)