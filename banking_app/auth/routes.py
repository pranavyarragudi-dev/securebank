from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from banking_app.auth import bp
from banking_app.models import User, Role, Account
from banking_app.forms import LoginForm, RegistrationForm
from banking_app import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('customer.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page:
                if user.is_admin():
                    next_page = url_for('admin.dashboard')
                else:
                    next_page = url_for('customer.dashboard')
            return redirect(next_page)
        flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Get customer role
        customer_role = Role.query.filter_by(name='customer').first()
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            role_id=customer_role.id
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        # Create a default checking account
        account = Account(
            account_type='checking',
            balance=0.0,
            user_id=user.id
        )
        db.session.add(account)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
