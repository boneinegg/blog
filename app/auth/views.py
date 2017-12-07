from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_user
from ..models import User
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login_html')
