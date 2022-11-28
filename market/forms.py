from flask_wtf import FlaskForm # klasa pomocu koje mozemo praviti forme od klasa
from wtforms import StringField, PasswordField, SubmitField # pomocu ovih klasa koje dolaze iz FlaskForm, kreiramo atribute klase da budu kao input dijelovi forme
# good stuff fr fr

class RegisterForm(FlaskForm):
    username = StringField(label='User Name:')
    email_address = StringField(label='Email Address:')
    password1 = PasswordField(label='Password:') # posebno polje od wtf za passworde
    password2 = PasswordField(label='Confirm Password:') # za "confirm password" ono da budu isti
    submit = SubmitField(label='Create Account') #za submit dugme