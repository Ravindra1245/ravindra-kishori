from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/login')
def login():
    return 'login, World'

@app.route('/signup')
def signup():
    return 'signup, World'

@app.route('/contact')
def contact():
    return 'contact, World'

@app.route('/history')
def history():
    return 'history, World'