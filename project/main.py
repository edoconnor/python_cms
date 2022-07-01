from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
from . import db
from .models import Blogpost
from datetime import datetime

main = Blueprint('main', __name__)


@main.route("/")
def index():
    date = datetime.now()
    blogposts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template("index.html", blogposts=blogposts, date=date)

# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', name=current_user.name)

@main.route('/<int:blogpost_id>/')
def blogpost(blogpost_id):
    blogpost = Blogpost.query.get_or_404(blogpost_id)
    return render_template('blogpost.html', blogpost=blogpost)

# @main.route("/delete/<int:blogpost_id>/", methods=['POST'])
# def delete(blogpost_id):
#     blogpost = Blogpost.query.get_or_404(blogpost_id)
#     db.session.delete(blogpost)
#     db.session.commit()
#     return redirect(url_for("main.index"))
