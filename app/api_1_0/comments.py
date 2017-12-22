from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
from ..models import User, AnonymousUser
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    if email == '':
        g.current_user = AnonymousUser()
        return True
    user = User.query.filter_by(email=email).first()

