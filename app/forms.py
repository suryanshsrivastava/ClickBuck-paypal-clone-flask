from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, SelectField, DateField
from wtforms.validators import Email, InputRequired, Length


# Login and Register Forms
class LoginForm(FlaskForm):
    # TODO Validate phone number
    phone = IntegerField('PhoneNumber', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    phone = IntegerField('Phone Number', [InputRequired()])
    name = StringField('Full Name', [InputRequired()])
    email = StringField('E-mail', [InputRequired(), Email()])
    password = PasswordField('Password', [InputRequired()])
    type = SelectField('Account Type', choices=[('personal', 'Personal'), ('business', 'Business')])
    submit = SubmitField("Register")


class TransactForm(FlaskForm):
    add = IntegerField('Add Money')
    addbutton = SubmitField('Add')
    pay = IntegerField('Pay Money')
    payee = IntegerField('Enter Phone Number')
    paybutton = SubmitField('Pay')
    receive = IntegerField('Receive Money')
    receivebutton = SubmitField('Receive')

class SearchFilterForm(FlaskForm):
    fromdate = DateField('From')
    todate = DateField('To')
    filter = SubmitField('Filter By Date')