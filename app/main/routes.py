# Routes are the different URLs that the application implements.
# The functions below handle the routing/behavior.

from flask import render_template, flash, redirect, url_for
from app.main import bp
from app.constants import AccountType
from app.main.forms import JobPostForm
from flask_login import current_user, login_required
from app.models import User, SeekerProfile, CompanyProfile


## TODO Routes needed for editing profile page, searching, sending messages, etc.

@bp.route("/")
@bp.route("/index")
def index():
    """ Home page """
    return render_template("index.html", title="Home")


@bp.route('/profile')
@login_required
def profile():
    """ Displays profile based on the current user's account type """
    # query user accounts for "current_user"'s ID
    user = User.query.filter_by(id=current_user.get_id()).first()
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


@bp.route("/postjob", methods=['GET', 'POST'])
@login_required
def postjob():
    """ New job page; non-company users will be redirected to the homepage (as a safety measure) """
    user = User.query.filter_by(id=current_user.get_id()).first()
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