from app import db



class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	login = db.Column(db.String(64), index = True, unique = True)
	password = db.Column(db.String(120), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
   
	def __repr__(self):
		return '<User %r>' % (self.login)
	
	def is_active(self):
		return True

	def get_id(self):
		return self.id
		
	def is_authenticated(self):
		"""Return True if the user is authenticated."""
		return True

	def is_anonymous(self):
		"""False, as anonymous users aren't supported."""
		return False

tags = db.Table('tags',
	db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
	db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(150), index = True)
	preview = db.Column(db.String(500), index = True)
	full = db.Column(db.Text(), index = True)
	date = db.Column(db.DateTime(), index = True)
	tags = db.relationship('Tag', secondary=tags,
	    backref=db.backref('posts', lazy='dynamic'))

	def __repr__(self):
		return '<Title %r>' % (self.title)


class Tag(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	text = db.Column(db.String(50), index = True, unique=True)

	def __repr__(self):		
		return str(self.text)

	def __init__(self, txt):
		self.text = txt

class About(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text(), index = True)

	def __repr__(self):
		return (self.body)