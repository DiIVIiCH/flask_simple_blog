from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField, TextAreaField, PasswordField
from wtforms.validators import Required, Length

class RegisterForm(FlaskForm):
	login = TextField('login',validators = [Required()])
	password = PasswordField('password',validators = [Required()])
	email = TextField('email',validators = [Required()])


class LoginForm(FlaskForm):
	login = TextField('login',validators = [Required()])
	password = PasswordField('password',validators = [Required()])
	remember_me = BooleanField('Remember me', default = False)


class PostForm(FlaskForm):
	title = TextField('title',validators =[Required(), Length(max=150)])
	preview = TextAreaField('preview',validators =[Required(), Length(max=500)])
	full = TextAreaField('full',validators =[Required()])
	tags = TextField('tags',validators =[Required()])

class AboutForm(FlaskForm):
	body = TextAreaField('body',validators =[Required()])