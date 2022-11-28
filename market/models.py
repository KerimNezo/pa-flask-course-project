from market import db

class User(db.Model):
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