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
    
    # GET
    if request.method == 'GET':
        return render_template('singup.html')
    
    # POST
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # check box's Not Empty
        if not email or not username or not password:
            return render_template("singup.html",message='Error: Please Full The Box')

        return render_template("singup.html",success='Register Complete')

    



@app.route('/login')
def login():
    return render_template('index.html')