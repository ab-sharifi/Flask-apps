from flask import Flask, render_template, request ,url_for,session 
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


@app.route('/login',methods=['POST','GET'])
def login():
    # GET
    if request.method == 'GET':
        return render_template('login.html')
    # POST
    if request.method == 'POST':
        username =request.form.get('username')
        password =request.form.get('password')
        password_re =request.form.get('password-re')

        if not password or not password or not password_re:
            return render_template('login.html.html',message='Please Complete Field ')


@app.route('/singin')
def singin():
    return render_template('singin.html')