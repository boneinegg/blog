from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm


@main.route('/')
def index():
    return render_template('index.html')

from ..decorators import admin_required, permission_required

from ..models import Permission
from flask_login import login_required

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"
