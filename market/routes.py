from market import app
from flask import render_template
from market.models import Item
from market.forms import RegisterForm

@app.route("/") #dekorator ide liniju prije funkcije i govori nam na kojem url-u će se 
@app.route("/home") #funckija dole brine o dva url. Ima smisla da bude home page u oba slucaja
# prikazati html kod(funkcija) "/" je homepage
def home_page(): # check navbar in base.html za imena funkcija
    return render_template("home.html") # po konvenciji je da se stvori templates folder za sav html kod

@app.route("/market")
def market_page():
    items = Item.query.all() #svi itemi spaseni u bazi
    return render_template("market.html", items=items) #Ovaj podatak dobavljamo putem varijable
    # {{ item_name }}

@app.route("/register")
def register_page():
    form = RegisterForm()
    return render_template("register.html", form=form)
# za formu nam treba key, koji se nalazi u __init__,py on nam tehnicki daje layer
# sigurnosti za forme, jer ipak s formama dajemo da ubacuju real podatke u nasu bazu
# which we need to secure 