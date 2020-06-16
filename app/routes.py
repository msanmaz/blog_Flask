import requests, json
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, ProfileEditForm
from app.models import User, Post
from flask_login import logout_user, login_required
from datetime import datetime


def getSearchURL(q):
    try:
        import urlparse
        from urllib import urlencode
    except:  # For Python 3
        import urllib.parse as urlparse
        from urllib.parse import urlencode

    url = "https://newsapi.org/v2/everything?"
    params = {'q': q, 'apiKey': 'be4af77aa1f8424f9f31dd14c71503f9'}

    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)


@app.route('/')
@app.route('/index')
@login_required  # doesnt allow without login
def index():
    return render_template('index.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        newUser = User(username=form.username.data, email=form.email.data)
        newUser.set_password(form.password.data)
        db.session.add(newUser)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # flask-login if the user already logged in
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():  # flask-login check on submit
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):  # if user not exist and password check
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)  # login flask
        next_page = request.args.get('next')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/news', methods=['GET'])
def news():
    q = request.args.get('q')
    # queryUpdate = request.get_json()['sweden']
    print(q)
    r = requests.get(getSearchURL(q))
    data = r.json()
    return jsonify(data)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html', user=user)


@app.before_first_request
def before_req():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/editprofile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileEditForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Your profile has been updated.')
