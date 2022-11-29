from flask_wtf import FlaskForm # klasa pomocu koje mozemo praviti forme od klasa
from wtforms import StringField, PasswordField, SubmitField # pomocu ovih klasa koje dolaze iz FlaskForm, kreiramo atribute klase da budu kao input dijelovi forme
# good stuff fr fr
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError #Importamo 
from market.models import User # ovo imporatamo da mozemo provjeriti da li vec postoji user sa unique atributima koje mi trenutno pokusavamo registrirati
#built-in klasu Length koja brine i duzini atributa u formi
#EqualTo koji prima parametar i provjerava je li parametar jednak sa vrijednostcu polja u kojem je EqualTo
#Email provjerava je li value polja email
#DataRequired provjerava da li u polju uopste ima ista napisano

# kako se ovaj validate_username() uopste zove, gdje se zove u kodu?
# e pa moj dobri prijatelju, its called Validators Library
# ukratko, mozemo funkcije name-at na poseban nacin i onda FlaskForm klasa se pobrine za ostalo
# time sto smo funkciju nazvali "validate_username", FlaskForm pregleda sve funkcije koje imaju prefix "validate_" i onda provjerava ostatak imena funkcije
# i onda trazi da li postoji bar polje sa tim imenom nakon prefixa (imamo polje dole u klasi RegisterForm koje se zove username)
# na ovaj nacin FlaskForm klasa zna validate-a_username (wordplay, znat ce flask da mora validateat username) jer imamo field koji se zove username
# zato trebamo paziti kako unosimo imena polja/funkcija, da flask moze razumijeti da treba na vakat executetat validacijsku funkciju
class RegisterForm(FlaskForm):
    # ako hocemo vise validacija po polju, moramo praviti listu validacija
    # validate_username hvata error unique polja prije nego sto dodju do sqlalchemy, odnosno ovako se mi 
    # brinemo i nosame kodu :D error unique polja, npr ako svaki username mora biti unique, a ti uneses na registeru username koji postji
    # bacit ce ti error
    def validate_username(self,username_to_check): # username_to_check je username koji zelimo provjeriti da li postoji
        # .first() pisemo jer User.query.filter_by() nam vraca objekat, te da bismo njemu pristupili treba nam .first()
        # ODNOSNO, AKO nam ovaj query, vrati objekat, a to mu je cilj, to znaci da postoji vec user sa username-om koji pokusavamo unijeti
        user = User.query.filter_by(username=username_to_check.data).first() # ovaj query filtrira kroz sve objekte klase User i gleda da li iko ima isti username
        # kao username_to_check, tj onaj koji mi zelimo provjeriti pri pregistraciji da li postoji
        if user: # ovo provjerava da user nije null, odnosno,ako je true, ima neki user
            raise ValidationError('Username already exists! Please try a different username')
    
    def validate_email_address(self,email_address_to_check): #potpuno isti princip kao za username
        
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already exists! Please try a different email address')
    
    username = StringField(label='User Name:', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()]) # posebno polje od wtf za passworde
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account') #za submit dugme