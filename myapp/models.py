from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import db,  login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Permission:
	FOLLOW = 0x01
	COMMENT = 0x02
	WRITE_ARTICLES =0x04
	MODERATE_COMMENTS = 0x08
	ADMINISTER = 0x80

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key = True,index=True)
	name = db.Column(db.String(64), unique = True)
	users = db.relationship('User', backref='role', lazy='dynamic')
	permission = db.Column(db.Integer)
	default = db.Column(db.Boolean, default=False, index=True)
		
	
	def __repr__(self):
		return '<Role, %s>' % self.name
	@staticmethod
	def insert_roles():
		roles={
			'User':(Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES , True),
			'Moderator':(Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES 
						| Permission.MODERATE_COMMENTS, False),
			'Administrator':(0xff, False)
			}

		for r in roles:
			role= Role.query.filter_by(name=r).first()
			if role is None:
				role=Role(name=r)
			role.permission=roles[r][0]
			role.default=roles[r][1]
			db.session.add(role)
		db.session.commit()




class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean, default = False)
	temp_email = db.Column(db.String(64),unique=True)

	@property
	def password(self):
		raise AttributeError('password is not readable')

	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User>,%s'  % self.username

	
	def generate_confirmation_token(self, expiration = 3600):
		s = Serializer(	current_app.config['SECRET_KEY'], expiration )
		return s.dumps({ 'confirm' : self.id })

	def confirm(self,token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False

		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True
	
	def generate_reset_token(self, expiration = 3600):
		s = Serializer( current_app.config['SECRET_KEY'], expiration )
		return s.dumps({'reset' : self.id })
	
	def reset_password(self,token,new_password):
		s = Serializer( current_app.config['SECRET_KEY'] )
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('reset') != self.id:
			return False
		self.password = new_password
		db.session.add(self)
		return True
	
	def generate_reset_email_token(self, expiration = 3600):
		s= Serializer( current_app.config['SECRET_KEY'], expiration)
		return s.dumps( {'reset_email': self.id} )

	def reset_email(self,token):
		s = Serializer( current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('reset_email') != self.id:
			return False
		self.email = self.temp_email
		db.session.add(self)
		return True


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
