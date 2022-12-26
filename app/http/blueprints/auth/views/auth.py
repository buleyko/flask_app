from flask import (render_template, redirect, url_for, request, flash, current_app,)
from app.http.blueprints.auth import bp_auth
from app.vendors.helpers.url import is_safe_url
from app.vendors.helpers.mail import get_register_mail
from werkzeug.security import generate_password_hash
from flask_babel import lazy_gettext as _l
from app.vendors.helpers.config import cfg
from app.vendors.helpers.token import check_user_token
from flask_babel import _
from app.extensions import db
from flask_login import (
    login_user, 
    logout_user,
    current_user,
)
from app.http.blueprints.auth.forms import (
    LoginForm, 
    RegisterForm,
)
from app.events.set.auth import ( 
    signin_signal,
    signup_signal, 
    signout_signal, 
)
from app.services.celery.tasks import send_email
from app.models import User


__all__ = (
	'signin', 
	'signup',
    'signout',
    'account_activate',
)


@bp_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    ''' Sign up '''
    form = LoginForm()
    if form.validate_on_submit():
        ''' After Login Form Validation '''
        curr_user = db.session.execute(
            db.select(User).filter_by(email=form.email.data)
        ).scalar()
        if curr_user is None or not curr_user.check_passwd(form.password.data):
            flash(_l(u'Invalid user email or password', category='warning'))
            return redirect(url_for('auth.signin'))

        signin_signal.send(current_app, username=curr_user.username)

        _next = request.args.get('next')
        if not is_safe_url(_next):
            return flask.abort(400)
    
        login_user(curr_user, remember=form.remember_me.data)
        return redirect(_next or url_for('admin.dashboard'))

    return render_template('auth/login.html', 
        form = form
    )


@bp_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    ''' Sign in '''
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            username = form.username.data,
            email = form.email.data,
            password = generate_password_hash(form.password.data),
            is_activated = False,
        )
        new_user.save()

        try:
            # send_async_email.delay(email_data)
            email_data = get_register_mail(new_user, '/srv/mail/register.html')
            send_email.apply_async(
                args=[email_data], 
                countdown=60
            )
            flash(_l(u'Check your mail', category='success'))
            signup_signal.send(current_app, username=new_user.username)
        except:
            flash(_l(u'Email not sent', category='warning'))

        return redirect(url_for('prime.home'))
    return render_template('auth/register.html', 
        form = form
    )


@bp_auth.route('/signout/', methods=['GET'])
def signout():
    ''' Sign out '''
    username = current_user.username
    logout_user()
    signout_signal.send(current_app, username=username)
    return redirect(url_for('prime.home'))


@bp_auth.route('/account_activate/<uidb64>/<token>/', methods=['GET'])
def account_activate(uidb64, token):
    user = User.get_by_uid(uidb64)
    print(check_user_token(user, token))
    if user is not None and check_user_token(user, token):
        user.is_activated = True
        user.save()
        flash(_l(u'Account activated', category='success'))
        return redirect(url_for('auth.signin'))
    else:
        flash(_l(u'Activation error', category='warning'))
        return redirect(url_for('prime.home'))