from market import app
from flask import render_template, redirect, url_for #redirect sluzi da usmjeri korisnika na drugu stranicu jer je now logged
from market.models import Item, User
from market.forms import RegisterForm
from market import db #db mogu importovati direktno iz marketa jer se db nalazi u dundur fileu __init__

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
                              password_hash=form.password1.data)
        db.session.add(user_to_create) #dodaje instancu klase koja je primila podatke iz forme
        db.session.commit() # ovo su naredbe koje smo prije rucno u cmd-u unosili da korisnike unesemo
        return redirect(url_for('market_page')) #legit kao u base.html u navbaru objasnjenje, da ne bude hard codirano
    #ako neka validacije padne(nije uneseno kako smo napisalo s validacijama) fail ce biti registrovan ovdje
    if form.errors != {}: # ako ima(jer nije prazan) errora od validacije (ljevicaste jer je form.errors dictionary)
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')
            # meni ne pokazuje errore u cmd-u idk why, ali validacija radi tj ne spasava lose usere u bazu, sto je dobro
    return render_template("register.html", form=form)
# za formu nam treba key, koji se nalazi u __init__,py on nam tehnicki daje layer
# sigurnosti za forme, jer ipak s formama dajemo da ubacuju real podatke u nasu bazu
# which we need to secure