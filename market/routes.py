from market import app
from flask import render_template, redirect, url_for, flash #redirect sluzi da usmjeri korisnika na drugu stranicu jer je now logged
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from market import db #db mogu importovati direktno iz marketa jer se db nalazi u dundur fileu __init__
from flask_login import login_user

@app.route("/") #dekorator ide liniju prije funkcije i govori nam na kojem url-u će se prikazati 
@app.route("/home") #funckija dole brine o dva url. Ima smisla da bude home page u oba slucaja
# prikazati html kod(funkcija) "/" je homepage
def home_page(): # check navbar in base.html za imena funkcija
    return render_template("home.html") # po konvenciji je da se stvori templates folder za sav html kod

@app.route("/market")
def market_page():
    items = Item.query.all() #svi itemi spaseni u bazi
    return render_template("market.html", items=items) #Ovaj podatak dobavljamo putem varijable
    # {{ item_name }}

@app.route("/register", methods=['GET', 'POST'])# ovu listu ubacujemo da nasa ruta moze handlat post i get metode
def register_page():
    form = RegisterForm() #klasa iz forms.py
    if form.validate_on_submit(): # what happens when user submits a 'create account' button
        #ovaj if postoji da provjer 
        # 1. da je korisnik kliknuo dugme
        # 2. da je korisnik unio ispravne podatke(radimo to pomocu validacija)
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        # stavili smo u User klasi ovdje password umjesto passwrod_hash sto je bilo
        # jer sada ovaj password moze ici u models.py @password.setter gdje ce se izvrsiti funkcija password
        
        db.session.add(user_to_create) #dodaje instancu klase koja je primila podatke iz forme
        db.session.commit() # ovo su naredbe koje smo prije rucno u cmd-u unosili da korisnike unesemo
        return redirect(url_for('market_page')) #legit kao u base.html u navbaru objasnjenje, da ne bude hard codirano
    #ako neka validacije padne(nije uneseno kako smo napisalo s validacijama) fail ce biti registrovan ovdje
    if form.errors != {}: # ako ima(jer nije prazan) errora od validacije (ljevicaste jer je form.errors dictionary)
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
            # get_flashed_message u base.html prima i kategoriju, odnosno napisali smo u njoj parametar da mozemo biti sa kategorijama
            # zato saljemo category="danger", danger jer bootstrap ima klase tipa danger, skontat ces kad pogledas taj kod u html. ugl salje danger
            # kao varijablu, da se prepozna u klasi i da bootstra dobije dobar opis za klasu
            # flash builtin funkcija je bolji print()?
    return render_template("register.html", form=form)
# za formu nam treba key, koji se nalazi u __init__,py on nam tehnicki daje layer
# sigurnosti za forme, jer ipak s formama dajemo da ubacuju real podatke u nasu bazu
# which we need to secure

@app.route("/login", methods=['GET', 'POST'])
def login_page(): #what happens when I press 'sign in' hmm...
    form = LoginForm()
    if form.validate_on_submit(): # treba provjeriti sada dvije stvari 1. da korisnik postoji 2. da je unio dobru sifru za acc 
        #return redirect(url_for('market_page'))
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)