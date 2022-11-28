from flask import Flask, render_template 
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'fba57affcb5e82a19bc851fa'
db = SQLAlchemy(app)

from market import routes