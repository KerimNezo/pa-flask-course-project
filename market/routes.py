from market import app
from flask import render_template, redirect, url_for, flash, request #redirect sluzi da usmjeri korisnika na drugu stranicu jer je now logged
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db #db mogu importovati direktno iz marketa jer se db nalazi u dundur fileu __init__
from flask_login import login_user, logout_user, login_required, current_user
# current_user je built-in objekat koji nam govori valjda koji je trenutni user logged in0
# login required nam sluzi da provjeri da li je user logged-in, i u zavisnosti od tog if-a
# aplikacija ce ga poslati na razlicito mjesto

@app.route("/") #dekorator ide liniju prije funkcije i govori nam na kojem url-u će se prikazati 
@app.route("/home") #funckija dole brine o dva url. Ima smisla da bude home page u oba slucaja
# prikazati html kod(funkcija) "/" je homepage
def home_page(): # check navbar in base.html za imena funkcija
    return render_template("home.html") # po konvenciji je da se stvori templates folder za sav html kod

@app.route("/market", methods=['GET','POST']) #ok, idemo na market
@login_required # but, ali jesi li loged-in ? rjesenjeu __init__ line12, ugl
# tamo smo nastimali da korisnika posalje na login_page ako on vec nije logged-in a pokusa uci u market
# line 13 se brine da ne bude ruzno napisan tekst "pls log in to acces", daje mu bootstrap kategoriju, we talked about this man
def market_page():
    purchase_form = PurchaseItemForm() #ovdje se obavlja kupovina
    selling_form = SellItemForm() #ovdje se obavlja prodaja
    if request.method == "POST": # radi isto kao validate on submit
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item') # ova varijabla sada dobija naziv itema koji smo kupili
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object: #ako postoji
            if current_user.can_purchase(p_item_object): #provjerava da li korisnika ima $$ da kupi item
                p_item_object.buy(current_user) # vrsi kupovinu.Nalazi se u Item modelu
                flash(f"Congratulashions! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        
        #Sell Item Logic
        sold_item = request.form.get('sold_item') # treba sold_item
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET": 
        # ovo smo dodatno napisali da nemamo confirm resubmision output koji vidimo na svakom reload-u stranice
        items = Item.query.filter_by(owner=None) # lista sve iteme spaseni u bazi
        owned_items = Item.query.filter_by(owner=current_user.id) #lista sve iteme koje logged korisnik posjeduje

        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)
        # ove podatke, items i purchase_form saljemo u market.html da se mogu koristiti, same w selling, ovako buttoni ferceraju



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
        login_user(user_to_create) #logina usera da skrati posao
        flash(f"Account created successfully! You are not logged in as {user_to_create.username}", category='success')
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

@app.route("/logout")
def logout_page():
    logout_user() #iz flask_login paketa/biblioteke, legit samo logouta
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))