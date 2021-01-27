from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    IntegerField, DateTimeField, TimeField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class AddeventsForm(FlaskForm):
    date = DateField('Date of event (format: yyyy-MM-dd )', format='%Y-%m-%d',
                     default=datetime.now, validators=[DataRequired()])
    time = TimeField('Time of event (format: HH:mm:ss)', format='%H:%M:%S', default=datetime.now,
                         validators=[DataRequired()])
    category = RadioField('Select Event Type', choices=[(0, "event"), (1, "deadline")], default=0,
                          validators=[DataRequired()])
    event = StringField('Event Description', validators=[DataRequired()])
    submit = SubmitField('Upload')
