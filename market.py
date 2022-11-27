from flask import Flask #import-amo flask instancu iz flask paketa
app = Flask(__name__) #incijaliziramo instancu Flaska sa argumentom
# __name__ (built-in var, referira na lokalni py file s kojim radimo)

@app.route("/") #dekorator ide liniju prije funkcije i govori nam na kojem url-u će se 
# prikazati html kod(funkcija) "/" je homepage
def hello_world():
    return "<h1>Hello World</h1>"

@app.route("/about/<username>") #dinamic routes, rute koje primaju varijable koje postaju dio linka
# upamti kako se ponasaju
def about(username): # ova funkcija handle-a sve requeste koji dođu na ovu rutu koja je u dekoratoru 
    return f"<h1>This is the about page of {username}</h1>"
