from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        InputRequired(), 
        Length(min=4, max=20),
        Regexp('^[A-Za-z0-9]+$', message="Username must contain only letters and numbers.")
    ])
    password = PasswordField('Password', validators=[
        InputRequired(), 
        Length(min=8, max=20)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(), 
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')
