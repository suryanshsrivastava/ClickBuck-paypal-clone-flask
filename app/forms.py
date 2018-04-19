from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import Email, InputRequired, Length


# Login and Register Forms
class LoginForm(FlaskForm):
    # TODO Validate phone number
    phone = IntegerField('PhoneNumber', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=15,
                                                                             message="Insufficient password length")])
    remember = BooleanField('remember me')
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    phone = IntegerField('PhoneNumber', validators=[InputRequired()])
    name = StringField('name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('password', validators=[InputRequired()])
    submit = SubmitField("Register")