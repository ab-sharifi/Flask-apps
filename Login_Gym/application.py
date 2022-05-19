from flask import Flask, render_template ,url_for,session 
from flask_session import Session
import sqlite3 

app = Flask(__name__)

# config session 
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/singin')
def singin():
    return render_template('singin.html')