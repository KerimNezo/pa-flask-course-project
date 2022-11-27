from flask import Flask, render_template 
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app) 

class Item(db.Model): #buduci da je Item klasa izvedena iz klase Model, to bazi govori da je Item klasa model
    id = db.Column(db.Integer, primary_key=True) #treba pk
    name = db.Column(db.String(length=30), nullable=False, unique=True) #name je kolona u bazi, koja je tipa string 
    # ima max 30charactera, ne smije biti null, te je ime itema unique
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)#barcode je string jer se s njim nece
    # raditi nikakve kalkulacije, vec samo postoji
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'

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