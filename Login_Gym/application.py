from flask import Flask, render_template ,url_for 


app = Flask(__name__,static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')