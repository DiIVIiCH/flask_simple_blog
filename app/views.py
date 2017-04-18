from flask import render_template, redirect, abort, url_for, g, request, flash, session
from app import app, db, lm
from sqlalchemy import update, desc
from .forms import RegisterForm, LoginForm, PostForm, AboutForm
from .models import User, Post, Tag, About
from flask_login import login_user, logout_user, current_user, login_required
import datetime
from urllib.parse import urlparse, urljoin
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def index():
	page_id = int(request.args.get('page', 1))
	post_id = request.args.get('post', -1)
	tag = request.args.get('tag', '')

	tags = tags_query()
	tags = tags[:10]

	if post_id != -1:
		post = Post.query.get(post_id)
		return render_template("post.html", post=post, tags=tags)

	if tag is not '':
		posts = Post.query.filter(Post.tags.any(text=tag)).order_by(desc(Post.date)).paginate(page_id, 20, False)
		return render_template("index.html", posts=posts, tags=tags)

	posts = Post.query.order_by(desc(Post.date)).paginate(page_id, 20, False)
	return render_template("index.html", posts=posts, tags=tags)

@app.before_request
def is_installed():
	if not session.get('installed', None):
		if url_for('static', filename='') not in request.path and request.path != url_for('install'):
			return redirect(url_for('install'))

@app.route('/install/', methods = ['GET', 'POST'])
def install():
	if session.get('installed', None):
		return redirect(url_for('index'))

	tags = []
	form = RegisterForm()
	if form.validate_on_submit():
		user = User()
		user.login = form.login.data
		user.password=generate_password_hash(form.password.data, method='sha256')
		user.email=form.email.data
		db.session.add(user)
		db.session.commit()
		session['installed'] = True
		return redirect(url_for('index'))
	return render_template("register.html", form = form, tags=tags)

@lm.user_loader
def user_loader(user_id):
	return User.query.get(user_id)

@app.route('/add_user/', methods = ['GET', 'POST'])
@login_required
def add_user():
	form = RegisterForm()
	tags = tags_query()
	tags = tags[:10]
	if form.validate_on_submit():
		user = User()
		user.login = form.login.data
		user.password=generate_password_hash(form.password.data, method='sha256')
		user.email=form.email.data
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template("register.html", form = form, tags=tags)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
	tags = tags_query()
	tags = tags[:10]
	form=LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(login = form.login.data).first()
		if check_password_hash(user.password, form.password.data):
			remember = form.remember_me.data
			login_user(user, remember)
			flash('Logged in successfully.')
			next = request.args.get('next')
			if not is_safe_url(next):
				return abort(400)
			return redirect(next or url_for('.index'))
	return render_template('login.html', form=form, tags=tags)

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/editor/', methods = ['GET','POST'])
@login_required
def editor():
	tags = tags_query()
	tags = tags[:10]

	post_id = request.args.get('post', -1)
	form = PostForm()
	if post_id != -1:
		post = Post.query.get(post_id)
	else:
		post = Post()

	if form.validate_on_submit():
		post.title = form.title.data
		post.preview = form.preview.data
		post.full = form.full.data
		post.tags = []

		tags=[]
		if (form.tags):
			tags = form.tags.data.split(',')
		for i, t in enumerate(tags):
			tmp  = t.strip()
			tags[i] = tmp

		for t in tags:
			obj = Tag.query.filter_by(text=t).first()
			if obj:				
				post.tags.append(obj)
			else:
				post.tags.append(Tag(t))

		if not post.date:
			post.date=datetime.datetime.now()
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('.index', post=post.id))
	return render_template("editor.html", form=form, post = post, tags=tags)

@app.route('/delete_post/')
@login_required
def delete_post():
	post_id = request.args.get('post', -1)
	form = PostForm()
	if post_id != -1:
		post = Post.query.get(post_id)
		if post:
			db.session.delete(post)
			db.session.commit()
	return redirect(url_for('.index'))

@app.route('/tags')
def tags():
	tags = tags_query()
	return render_template('tags.html', tags = tags)

@app.route('/about_author', methods = ['GET','POST'])
def author():
	tags = tags_query()[:10]
	about=About.query.get(2)
	if not about:
		about=About()
	form = AboutForm()
	if form.validate_on_submit():
		about.body = form.body.data
		db.session.add(about)
		db.session.commit()
	return render_template('/about_author.html', tags=tags, form=form, about=about)


@app.route('/about_blog', methods = ['GET','POST'])
def about_blog():
	tags = tags_query()[:10]
	about=About.query.get(1)
	if not about:
		about=About()
	form = AboutForm()
	if form.validate_on_submit():
		about.body = form.body.data
		db.session.add(about)
		db.session.commit()	
	return render_template('/about_blog.html', tags=tags, form=form, about=about)

def tags_query():
	tags = list(db.session.query(Tag, db.func.count(Post.id).label('total')).join(Post.tags).group_by(Tag.id).order_by('total DESC'))
	return tags

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc