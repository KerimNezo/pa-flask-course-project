from flask import Flask, render_template #import-amo flask instancu iz flask paketa(and whole lot more)
app = Flask(__name__) #incijaliziramo instancu Flaska sa argumentom
# __name__ (built-in var, referira na lokalni py file s kojim radimo)

@app.route("/") #dekorator ide liniju prije funkcije i govori nam na kojem url-u će se 
@app.route("/home") #funckija dole brine o dva url. Ima smisla da bude home page u oba slucaja
# prikazati html kod(funkcija) "/" je homepage
def home_page():
    return render_template("home.html") # po konvenciji je da se stvori templates folder za sav html kod

@app.route("/market")
def market_page():
    return render_template("market.html")