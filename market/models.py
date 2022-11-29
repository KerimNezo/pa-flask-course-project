from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

# Flask kao framework trazi dodatne metode da se hardkodirajum, da bi login mogao da funkcionise
# UserMixin je klasa koja dolazi iz flask_logina i koja sadrzi sve potrebne klase da budu dostupne
# nasem User Modelu, tj moramo dodatno inheritancu uradit, ili ti ga izvesti nesto iz UserMixin kase

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    #backref ce nam dozoviliti da ako zelimo znati vlasnika nekog itema, mozemo tu informaciju dobiti od item-a
    # klasicno je da ako zelimo znati iteme od usera, uzmemo usera i vidjet cemo iteme, ali nemozemo isto uraditi obrnuto.
    # da od itema dobijemo ko je njegov user, jer tog nema Item modelu, ali s ovim mozemo 
    # ako ne stavimo lazy = True, SQLAlchemy nece uzezi sve objekte Itema u jednom "shotu?" bitno je tho

    @property # ovo ce nam ljepse ispisivati novac (stavljat ce zarez iza svake trece cifre)
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property #design pattern koji nam dozvoljava da dodamo nove funkcionalnosti na postojeci objekat bez da modifikuje njegovu strukturu
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    # zbog ovog nam se hashira password u user = User(...), u routes file-, jer se zove tamo password, kao ovdje i dekorator i funkcije (setter mainly)

    def check_password_correction(self, attempted_password): 
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

# ovdje parametar a_pass je ono sto unesemo u login
# provjerava da li je raw string koji smo unijeli na loginu u polje sifra
# jednak hashiranoj sifri koja je spasena
# prvo ide hash, onda string iz logina
# prvobitno nije bio return nego if pa bi on vracao true ili false, ovako imamo istu
# stvar sa manje koda. Space efficiency, just like my comments :D
# ova funkcija sad samo vrati True/False

class Item(db.Model): #buduci da je Item klasa izvedena iz klase Model, to bazi govori da je Item klasa model
    id = db.Column(db.Integer, primary_key=True) #treba pk
    name = db.Column(db.String(length=30), nullable=False, unique=True) #name je kolona u bazi, koja je tipa string 
    # ima max 30charactera, ne smije biti null, te je ime itema unique
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)#barcode je string jer se s njim nece
    # raditi nikakve kalkulacije, vec samo postoji
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id')) #veze se za prvi kolonu u Useru (id)
    #Colona owner je povezana sa svakim unique redom koji se spasen u User model

    def __repr__(self):
        return f'Item {self.name}' # ovo je samo za konzolni ispis Item.query.all()