from flask_wtf import FlaskForm # klasa pomocu koje mozemo praviti forme od klasa
from wtforms import StringField, PasswordField, SubmitField # pomocu ovih klasa koje dolaze iz FlaskForm, kreiramo atribute klase da budu kao input dijelovi forme
# good stuff fr fr
from wtforms.validators import Length, EqualTo, Email, DataRequired #Importamo 
#built-in klasu Length koja brine i duzini atributa u formi
#EqualTo koji prima parametar i provjerava je li parametar jednak sa vrijednostcu polja u kojem je EqualTo
#Email provjerava je li value polja email
#DataRequired provjerava da li u polju uopste ima ista napisano


class RegisterForm(FlaskForm):
    # ako hocemo vise validacija po polju, moramo praviti listu validacija
    username = StringField(label='User Name:', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()]) # posebno polje od wtf za passworde
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account') #za submit dugme