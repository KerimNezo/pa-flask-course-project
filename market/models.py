from market import db
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