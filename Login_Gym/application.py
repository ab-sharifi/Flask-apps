from flask import Flask, redirect, render_template, request ,url_for,session 
from flask_session import Session
from cs50 import SQL
import math

# create connection with data base
db = SQL('sqlite:///database.db')

app = Flask(__name__)

# config session 
app.config['SESSION_PERMANENT'] = False
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
        username = request.form.get('username')
        password = request.form.get('password')

        if not password or not username:
            return render_template('login.html',message='Please Complete The Fields')
        
        answer = db.execute('SELECT username from users WHERE username LIKE ?',username)
        if len(answer) != 0:
            answer = db.execute('SELECT password from users WHERE password == ?',hash(password))
            if len(answer) != 0:
                return redirect('homePage')
            else:
                return render_template('login.html',message='Password is Wring')
        else:
            return render_template('login.html',message='Username Not found')

@app.route('/singin',methods=['POST','GET'])
def singin():
    # GET
    if request.method == 'GET':
        return render_template('singin.html')

    # POST
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_re = request.form.get('password_re')
        email = request.form.get('email')
    
    # check to all field is Not empty
    if not username or not password or not password_re or not email:
        return render_template('singin.html',message='Please Complete Field ')
    
    # check if passwords are not match
    if password != password_re:
        return render_template('singin.html',message="Password's not Match! ")
    
    # check is Username is available in data base or Not
    answer = db.execute('SELECT username FROM users WHERE username LIKE ?',username)

    if len(answer) != 0 :
        return render_template('singin.html',message='This Username takes by another User')
    
    # if username is not in data base so we register user
    else:
        answer = db.execute("""INSERT INTO users ('username', 'password','email')
        VALUES (?,?,?) """,username,hash(password),email)
        session["name"] = hash(password)        
        return render_template('singin.html',success= 'Register complete')      

@app.route('/logout')
def logout():
    session["name"] = None
    return redirect('/')


@app.route('/homePage')
def homePage():
    temp = session['name']
    name  = db.execute('SELECT username FROM users WHERE password LIKE ?',temp)
    return render_template('homePage.html',name = name)
    
