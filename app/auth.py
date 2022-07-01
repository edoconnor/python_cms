from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Blogpost
from datetime import datetime

from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup')
@login_required
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
@login_required
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists!')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/profile')
@login_required
def profile():
    flash('You are logged in!', 'success')
    return render_template('profile.html', name=current_user.name)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please try again.', 'error')
        return redirect(url_for('auth.login'))

    elif user and check_password_hash(user.password, password):
        flash('You are logged in!', 'success')
        login_user(user, remember=remember)

    return redirect(url_for('auth.profile'))


@auth.route('/create')
@login_required
def create():
    return render_template('create.html')


@auth.route('/create', methods=['POST'])
@login_required
def create_post():

    title = request.form["title"]
    subtitle = request.form["subtitle"]
    author = request.form["author"]
    content = request.form["content"]
    image = request.form["image"]
    blogpost = Blogpost(title=title,
                        subtitle=subtitle,
                        author=author,
                        image=image,
                        content=content,
                        date_posted=datetime.now())

    db.session.add(blogpost)
    db.session.commit()

    return redirect(url_for('app.index'))


@auth.route('/edit/<int:blogpost_id>/', methods=('GET', 'POST'))
@login_required
def edit_post(blogpost_id):
    blogpost = Blogpost.query.get_or_404(blogpost_id)

    if request.method == 'POST':
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        author = request.form["author"]
        image = request.form["image"]
        content = request.form["content"]

        blogpost.title = title
        blogpost.subtitle = subtitle
        blogpost.author = author
        blogpost.image = image
        blogpost.content = content

        db.session.add(blogpost)
        db.session.commit()

        return redirect(url_for("app.index"))

    return render_template('edit.html', blogpost=blogpost)


@auth.route("/delete/<int:blogpost_id>/", methods=['POST'])
@login_required
def delete(blogpost_id):
    blogpost = Blogpost.query.get_or_404(blogpost_id)
    db.session.delete(blogpost)
    db.session.commit()
    return redirect(url_for("app.index"))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.index'))
