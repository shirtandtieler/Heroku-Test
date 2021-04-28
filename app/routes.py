# routes are the different URLs that the application implements
# "view functions" handle the routing
from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, RegisterForm


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login(): # sdlfjksdlkf
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('User {} performed registration for a {} account'.format(
            form.email.data, form.account_type.data))
        return redirect('/index')
    return render_template('register.html', title='Register', form=form)
