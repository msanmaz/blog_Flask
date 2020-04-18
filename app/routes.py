from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user
from app import app,db
from app.forms import LoginForm,RegistrationForm
from app.models import User
from flask_login import logout_user, login_required
from werkzeug.urls import url_parse




@app.route('/')
@app.route('/index')
@login_required #doesnt allow without login
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        newUser =User(username=form.username.data, email=form.email.data)
        newUser.set_password(form.password.data)
        db.session.add(newUser)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  #flask-login if the user already logged in
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): #flask-login check on submit
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data): #if user not exist and password check
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data) #login flask
        next_page = request.args.get('next')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))