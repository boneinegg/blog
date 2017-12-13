#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Role, User, Permission, Post
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

@manager.command
def test():
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

def make_shell_context():
	return dict(app=app, db=db, Role=Role, User=User,
				Permission=Permission, Post=Post)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def runserver():
	app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ == '__main__':
	manager.run()

