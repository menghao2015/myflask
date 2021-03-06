from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, ValidationError
from wtforms.validators import Required, Length,Regexp, Email
from ..models import Role,User,Post
from flask.ext.pagedown.fields import PageDownField

class CommentForm(Form):
	body = StringField('', validators=[Required()])
	submit = SubmitField('Submit')


class PostForm(Form):
	body = PageDownField("what's your mian ?", validators=[Required()])
	submit = SubmitField('submit')

class PostForm(Form):
	body = PageDownField("what's you mind on", validators=[Required()])
	submit = SubmitField('submit')

class NameForm(Form):
	name = StringField('what is you name', validators=[Required()])
	submit = SubmitField('submit')


class EditProfileForm(Form):
	name = StringField('Real name', validators=[Length(0,64)])
	locate = StringField('location', validators=[Length(0,128)])
	about_me = TextAreaField('About me')
	submit = SubmitField('submit')

class EditProfileAdminForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64),Email()])
	username = StringField('Username', validators=[Required(), Length(1,64), Regexp('^[a-zA-z0-9_.]*$', 0,
														'Username must have only letters, numbers, dots,underscores')])
	confirmed = BooleanField('Confiremd')
	role = SelectField('Role', coerce=int)
		
	name = StringField('Real name', validators=[Length(0,64)])
	locate = StringField('location', validators=[Length(0,128)])
	about_me = TextAreaField('About me')
	submit = SubmitField('submit')
	

	def __init__(self,user, *args, **kwargs):
		super(EditProfileAdminForm,self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self,field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered')

	def validate_username(self,field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('Usernmae already in use.')

