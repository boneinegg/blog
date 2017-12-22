from flask import jsonify
from app.exceptions import ValidationError
from . import api

def bad_request(message):
    respone = jsonify({'error': 'not found', 'message': message})
    respone.status_code = 404
    return respone

def forbidden(message):
    respone = jsonify({'error': 'forbidden', 'message': message})
    respone.status_code = 403
    return respone

def unauthorized(message):
    respone = jsonify({'error': 'unauthorized', 'message': message})
    respone.status_code = 401

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])