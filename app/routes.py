
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from app import app, bcrypt, db
from app.forms import RegisterForm, LoginForm, PasswordResetRequestForm, ResetPasswordForm
from app.models import User
from app.email import send_password_reset_mail

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        print(username, email, password)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, registeration success', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            #User exists and password matched
            login_user(user, remember=remember)
            flash('Login Success', category='info')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)

            return redirect(url_for('index'))
        flash('User not exists or password not matched', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/send_password_reset_request', methods=['GET', 'POST'])
def send_password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordResetRequestForm()
    print('form---->', form.validate_on_submit)
    if form.validate_on_submit:
        email = form.email.data
        print('email--->', email)
        user = User.query.filter_by(email=email).first()
        print('user---->', user)
        token = user.generate_reset_password_token()
        print('token--->', token)
        send_password_reset_mail(user, token)
        flash('Password reset request mail is sent, please check your email', category='info')
    return render_template('send_password_reset_request.html', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    return render_template('reset_password.html', form=form)

