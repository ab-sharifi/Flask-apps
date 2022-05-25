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
     return render_template('singup.html')


    



@app.route('/login')
def login():
    return render_template('index.html')