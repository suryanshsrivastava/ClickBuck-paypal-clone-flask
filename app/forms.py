from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectField
from wtforms.validators import Email, InputRequired, Length


# Login and Register Forms
class LoginForm(FlaskForm):
    # TODO Validate phone number
    phone = IntegerField('PhoneNumber', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    phone = IntegerField('Phone Number', validators=[InputRequired()])
    name = StringField('Full Name', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    type = SelectField('Account Type', choices=[('personal', 'Personal'), ('business', 'Business')])
    submit = SubmitField("Register")