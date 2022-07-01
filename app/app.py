from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from . import db
from .models import Blogpost
from datetime import datetime

app = Blueprint('app', __name__)

@app.route("/")
def index():
    date = datetime.now()
    blogposts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template("index.html", blogposts=blogposts, date=date)


@app.route('/<int:blogpost_id>/')
def blogpost(blogpost_id):
    blogpost = Blogpost.query.get_or_404(blogpost_id)
    return render_template('blogpost.html', blogpost=blogpost)
