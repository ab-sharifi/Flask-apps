from crypt import methods
from distutils.log import error
import sqlite3
from flask import Flask, render_template, redirect, request,session

def create_conn():
    conn = sqlite3.connect('data.db')
    return conn
    

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/singup',methods=['POST','GET'])
def singup():

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    if request.method == 'GET':
        return render_template('singup.html')

    if not username or not password or not email:
        return render_template('singup.html',message='Full The Form')
    



@app.route('/login')
def login():
    return render_template('index.html')