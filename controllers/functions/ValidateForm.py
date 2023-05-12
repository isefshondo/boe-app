from flask import Flask, redirect
import re

def validateForm(fullName, email, password, confirmPassword):
    nameValidate = not fullName and re.search(r"\d", fullName) and len(fullName) > 3
    emailValidate = not email and re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$'r'^[\w\.-]+@[\w\.-]+\.\w+$', email)
    passwordValidate = not password and len(password) > 8
    conPasswordValidate = confirmPassword == password

    if nameValidate and emailValidate and passwordValidate and conPasswordValidate:
        return {"message" : "Please check if they are all filled correctly"}
    else:
        return {"message" : "Congrats! You can go on"}