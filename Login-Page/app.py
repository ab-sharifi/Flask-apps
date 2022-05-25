from flask import Flask, render_template, redirect, request,session
from cs50 import SQL

 
db=SQL('sqlite:///data.db')

def validate(username):
    # username cannot start with number
    if username[0].isdigit():
        return False

    # check for sql injection 
    if '-' in username:
        return False

    # check for username created by number and alphabet
    for i in username:
        if not i.isnumeric() and not i.isalpha():
            return False
    
    return True


def validate_username(username):
    answer = db.execute("""
    SELECT username FROM users WHERE username LIKE ?""",(username))
    
    if len(answer) != 0:
        return False
    return True



def create_account(username,password,email):
    password =hash(password)
    ans=db.execute("""
    INSERT INTO users (username, password, email) VALUES (? ,? ,?)""",username,password,email)
    if not ans:
        return False
    return True



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
        
        # validate username is correct 
        if (not validate(username)):
            return render_template("singup.html",message='Username is Not Correct Username Cannot Start With Number or have Space Between it Username Should just have Number and Character')
        

        # validate username is not duplicate
        if (not validate_username(username)):
            return render_template("singup.html",message='Username Already Taked by another User :( ')

        # create user account
        if not create_account(email=email,username=username,password=password):
            return render_template("singup.html",message='Error Something Wring In Server Side :( ')

        return render_template("singup.html",success='Register Complete')
        
    



@app.route('/login')
def login():
    return render_template('index.html')