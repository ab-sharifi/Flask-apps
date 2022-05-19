from flask import Flask, render_template, request ,url_for,session 
from flask_session import Session
import sqlite3 

# create connection with data base
conn = sqlite3.connect('database.db')

# create a cursor for Data base
db = conn.cursor()

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
    return render_template('login.html')




@app.route('/singin',methods=['POST','GET'])
def singin():
    # GET
    if request.method == 'GET':
        return render_template('singin.html')

    username = ''
    password = ''
    password_re = ''
    email = ''
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
    answer = db.execute('SELECT username FROM users WHERE name LIKE ?',username)
    conn.commit()
    if len(answer) != 0 :
        conn.close()
        return render_template('singin.html',message='This Username takes bu another User')
    
    # if username is not in data base so we register user
    else:
        answer = db.execute("""INSERT INTO users ('username', 'password','email')
        VALUES (?,?,?) """,username,hash(password),email)
        conn.commit()
        conn.close()
        return render_template('singin.html',success= 'Register complete')      

