from flask import Flask
 
app = Flask(__name__, static_folder='static')
 
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '777c5eecb4130cec5b38376935b8edf8a27c352d89a2516c'
 
from app import views  # noqa