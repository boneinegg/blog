# __*__ coding: utf-8 __*__

import os
from flask import Flask
from flask import request, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail, Message
from flask_script import Manager, Shell
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from datetime import datetime
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'liupengpeng'
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '316786195@qq.com'
app.config['MAIL_PASSWORD'] = 'lp137..0!#'
app.config['BLOG_MAIL_SUBJECT_PREFIX'] = '管理员：'
app.config['BLOG_MAIL_SENDER'] = '316786195@qq.com'
app.config['BLOG_ADMIN'] = '316786195@qq.com'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
migrate = Migrate(app, db)
mail = Mail(app)

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username

class NameForm(Form):
	name = StringField('你的名字？', validators=[Required()])
	submit = SubmitField('提交')

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(to, subject, template, **kwargs):
	msg = Message(app.config['BLOG_MAIL_SUBJECT_PREFIX'] + subject, 
		sender=app.config['BLOG_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr

def make_shell_context():
	return dict(app=app, db=db, Role=Role, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@app.route('/', methods=['GET', 'POST'])
def home():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known'] = False
			if app.config['BLOG_ADMIN']:
				send_email(app.config['BLOG_ADMIN'], '新用户！',
					'mail/new_user', user=user)
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('home'))
	return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False), current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route('/signin', methods=['GET'])
def signin_form():
	return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
	username = request.form['username']
	password = request.form['password']
	if username == 'admin' and password == 'password':
		return render_template('sign_ok.html', username=username)
	else:
		return render_template('form.html', message = 'wrong username or password',
			username=username)

if __name__ == "__main__":
	manager.run()

