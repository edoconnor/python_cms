from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    content = db.Column(db.Text)
    image = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime(timezone=True),
                            server_default=func.now())

    def __repr__(self):
        return f"<Blogpost {self.id}>"


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup')
@login_required
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
@login_required
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists!')
        return redirect(url_for('signup'))

    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    flash('You are logged in!', 'success')
    return render_template('profile.html', name=current_user.name)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please try again.', 'error')
        return redirect(url_for('login'))

    elif user and check_password_hash(user.password, password):
        flash('You are logged in!', 'success')
        login_user(user, remember=remember)

    return redirect(url_for('profile'))


@app.route('/create')
@login_required
def create():
    return render_template('create.html')


@app.route('/create', methods=['POST'])
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

    return redirect(url_for('index'))


@app.route('/edit/<int:blogpost_id>/', methods=('GET', 'POST'))
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

        return redirect(url_for("index"))

    return render_template('edit.html', blogpost=blogpost)


@app.route("/delete/<int:blogpost_id>/", methods=['POST'])
@login_required
def delete(blogpost_id):
    blogpost = Blogpost.query.get_or_404(blogpost_id)
    db.session.delete(blogpost)
    db.session.commit()
    return redirect(url_for("index"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
def index():
    date = datetime.now()
    blogposts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template("index.html", blogposts=blogposts, date=date)


@app.route('/<int:blogpost_id>/')
def blogpost(blogpost_id):
    blogpost = Blogpost.query.get_or_404(blogpost_id)
    return render_template('blogpost.html', blogpost=blogpost)


if __name__ == '__main__':
    app.run()
