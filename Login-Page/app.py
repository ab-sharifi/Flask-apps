from flask import Flask, render_template, redirect, request,session,url_for
from cs50 import SQL
from flask_session import Session

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# connect with data base
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


# validate email form user in data base
def validate_username(username):
    answer = db.execute("""
    SELECT username FROM users WHERE username LIKE ?""",username)

    if len(answer) != 0:
        # username is exists
        return False
    # username does not exists
    return True


def validate_password(password):
    temp = hash(password)

    answer = db.execute("""
        SELECT * FROM users WHERE password = ?""",temp)

    if len(answer) != 0:
        # return True password is correct
        return True
    # otherwise password is not correct
    return False


# validate a email from user in data base
def validate_email(email):
    answer = db.execute("""
    SELECT email FROM users WHERE email LIKE ?""",email)

    if len(answer) != 0:
        return False
    return True


# create user in data base
def create_account(username,password,email):
    password =hash(password)
    ans=db.execute("""
    INSERT INTO users (username, password, email) VALUES (? ,? ,?)""",username,password,email)
    if not ans:
        return False

    return True

def fetch_data(username):
    answer = db.execute("""
    SELECT username,email FROM users WHERE username = ?
    """,username)
    return answer


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
            return render_template("singup.html",message='Username Already Take by another User :( ')

        # validate email of user
        if (not validate_email(email)):
            return render_template("singup.html",message='This Email Already Exists :( ')


        # create user account
        if not create_account(email=email,username=username,password=password):
            return render_template("singup.html",message='Error Something Wrong In Server Side :( ')

        session['username']= username
        session['email'] = email

        # Register complete redirect user to login page
        return redirect(url_for('login'))


@app.route('/login',methods=['POST','GET'])
def login():

    # GET
    if request.method == 'GET':

        if not session.get('username'):
            return render_template('login.html')

        return render_template('Profile.html',name=session.get('username'),email=session.get('email'))

    # POST
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # validate username input
        if validate(username) == False:
            return render_template("login.html",message='Username is Not Correct Username Cannot Start With Number or have Space Between it Username Should just have Number and Character')

        # validate is username is in the data base
        if (validate_username(username) == True):
            return render_template("login.html",message="Username does Not Exists !")

        # validate password is correct
        if (validate_password(password) == False):
            return render_template("login.html",message='Password is Wrong !')

        result = fetch_data(username)
        name = result[0].get('username')
        email = result[0].get('email')

        return render_template('Profile.html',email=email,name=name)

