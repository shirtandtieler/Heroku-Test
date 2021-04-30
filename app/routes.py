# routes are the different URLs that the application implements
# "view functions" handle the routing
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.constants import AccountType
from app.forms import LoginForm, RegisterForm, JobPostForm
from flask_login import current_user, login_user, logout_user, login_required

from app.models import Useraccount, SeekerProfile, CompanyProfile

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Handles the login page by showing and submitting the form """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Useraccount.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Handles the registration page by showing and submitting the form """
    form = RegisterForm()
    if form.validate_on_submit():
        user = Useraccount.query.filter_by(email=form.email.data).first()
        if user is not None:
            flash(f'User {form.email.data} is already registered!')
            return redirect(url_for('register'))
        # create new user and add to the database
        # TODO Bad practice to interface w/db directly. Replace with API
        user = Useraccount(account_type = form.account_type.data, email = form.email.data)
        user.set_password(form.password.data)  # hashes it
        db.session.add(user)

        ## TODO Add external trigger to create a seeker or company profile when user accounts are added (or change table structure)

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/profile')
@login_required
def profile():
    # query user accounts for "current_user"'s ID
    user = Useraccount.query.filter_by(id=current_user.get_id()).first()
    if user is None:
        flash(f'Could not find user!')
        return redirect(url_for('index'))
    flash(f'Found user with email: {user.email}')
    if user.account_type == AccountType.SEEKER:
        prof = SeekerProfile.query.filter_by(id=user.id).first()
        if prof is None:  # TODO should not happen unless auto-profile wasn't implemented
            _name = 'FIX ME'
        else:
            _name = (prof.first_name or 'ERROR') + ' ' + (prof.last_name or 'ERROR')
        return render_template('seeker/profile.html', fullname=_name)
    elif user.account_type == AccountType.COMPANY:
        prof = CompanyProfile.query.filter_by(id=user.id).first()
        if prof is None:  # TODO should not happen unless auto-profile wasn't implemented
            _name = 'FIX ME'
            _loc = 'IDK, USA'
            _url = 'https://error404.biz'
        else:
            _name = prof.name
            _loc = (prof.city+", " if prof.city else "") + prof.state
            _url = prof.website
        return render_template('company/profile.html', name=_name, citystate=_loc, url=_url)
    elif user.account_type == AccountType.ADMIN:
        return render_template('admin/profile.html')
    return redirect(url_for('index'))


@app.route("/postjob", methods=['GET', 'POST'])
@login_required
def postjob():
    user = Useraccount.query.filter_by(id=current_user.get_id()).first()
    if user is None:
        flash('Could not find user!')
        return redirect(url_for('index'))
    if user.account_type != AccountType.COMPANY:
        flash(f'Not a company!')
        redirect(url_for('index'))
    form = JobPostForm()
    if form.validate_on_submit():
        # TODO Add new job post to database
        # TODO redirect to page for newly created job posting
        flash(f'Mock-created job post: {form.title.data}')
        return redirect(url_for('index'))
    return render_template('company/newjobpost.html', form=form)