from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
from banking_app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Phone', validators=[Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class TransferForm(FlaskForm):
    to_account = StringField('To Account Number', validators=[DataRequired(), Length(min=10, max=10)])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01, max=5000)])
    description = TextAreaField('Description', validators=[Length(max=200)])

class DepositForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01, max=10000)])
    description = TextAreaField('Description', validators=[Length(max=200)])

class WithdrawalForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    description = TextAreaField('Description', validators=[Length(max=200)])

class CreateAccountForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[('checking', 'Checking'), ('savings', 'Savings')], 
                             validators=[DataRequired()])
    initial_deposit = FloatField('Initial Deposit', validators=[NumberRange(min=0)])
