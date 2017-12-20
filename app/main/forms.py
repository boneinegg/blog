from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class PostForm(FlaskForm):
	body = PageDownField('What\'s on your mind?', validators=[DataRequired()])
	submit = SubmitField('提交')

class EditProfileForm(FlaskForm):
	name = StringField('Real name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0,64)])
	about_me = TextAreaField('About_me')
	submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Length(1, 64),
											 Email()])
	username = StringField('Username', validators=[
		DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
											  'Usernames must have only letters, '
											  'numbers, dots or underscores')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role', coerce=int)
	name = StringField('Real name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0, 64)])
	about_me = TextAreaField('About_me')
	submit = SubmitField('Submit')

	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name)
							 for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def vaildate_email(self, field):
		if field.data != self.email and \
				User.query.filter_by(email=field.data).first():
			raise ValueError('Email already registered.')

	def validate_username(self, field):
		if field.data != self.username and \
				User.query.filter_by(username=field.data).first():
			raise ValueError('Username already in use.')



	
