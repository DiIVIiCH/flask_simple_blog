import os
from .app import app
from .database import db
from .login import lm
from flaskext.markdown import Markdown
from flask_bootstrap import Bootstrap

def create_app():

	lm.init_app(app)
	lm.login_view = "login"
	Markdown(app)
	db.init_app(app)
	Bootstrap(app)
	with app.test_request_context():
	        from .models import User, Tag, Post
	        db.create_all()
	from app import views
	
	return app



