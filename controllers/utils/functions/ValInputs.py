import re

def validateName(name):
    if not len(name) > 3:
        return {
            'status': False,
            'mensagem': 'O nome deve ter pelo menos 3 letras.'
        }
    if re.search(r'\d', name):
        return {
            'status': False,
            'mensagem': 'O nome não deve conter números.'
        }
        
    return {'status': True}

def validateEmail(email):
    emailPattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(emailPattern, email):
        return {
            'status': False,
            'mensagem': 'O dado fornecido não é um email.'
        }
    
    return {'status': True}

def validatePassword(password):
    if len(password) < 8:
        return {
            'status': False,
            'mensagem': 'A senha deve ter pelo menos 8 caracteres.'
        }
    if not re.search(r'[A-Z]', password) and not re.search(r'[a-z]', password):
        return {
            'status': False,
            'mensagem': 'A senha deve ter pelo menos um dígito minúsculo e maiúsculo.'
        }
    if not re.search(r'\d', password):
        return {
            'status': False,
            'mensagem': 'A senha deve ter pelo menos um dígito.'
        }
    
    return {'status': True}

def validateConfirmPassword(password, confirmPassword):
    if not password == confirmPassword and not len(password) == len(confirmPassword):
        return {
            'status': False,
            'mensagem': 'As senham não correspondem.'
        }
    return {'status': True}