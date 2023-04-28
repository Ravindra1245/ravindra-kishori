import pyrebase
from flask import Flask, render_template, request, session, redirect,url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = "secret_key"

firebaseConfig = {'apiKey': "AIzaSyBmjynphrpL1BTE3dYk01acBctYvtZHGi4",
                  'authDomain': "price-shraddha.firebaseapp.com",
                  'databaseURL': "https://price-shraddha-default-rtdb.firebaseio.com",
                  'projectId': "price-shraddha",
                  'storageBucket': "price-shraddha.appspot.com",
                  'messagingSenderId': "801214337523",
                  'appId': "1:801214337523:web:898bf9b5de63ff8ec44286",
                  'measurementId': "G-HKE64M5DSZ"}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Signup page
@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form['email']
    password = request.form['password']
    try:
        auth.create_user_with_email_and_password(email, password)
        user_data = {"password": password}
        db.child("users").child(email.replace(".", ",")).set(user_data)
        return redirect('/login')
    except:
        return render_template('signup.html', message="Email already exists")

# Login page
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        session['email'] = email
        session['password'] = password
        return redirect('/dashboard')
    except:
        return render_template('login.html', message="Invalid Credentials")

# Dashboard page
@app.route('/dashboard')
def dashboard():
    try:
        email = session['email']
        password = session['password']
        return render_template('dashboard.html', email=email, password=password)
    except KeyError:
        return redirect('/login')

# Logout page
@app.route('/logout')
def logout():
    session.pop("email", None)
    session.pop("password", None)
    return redirect(url_for("login"))

# Forgot password page
@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/forgot', methods=['POST'])
def forgot_post():
    email = request.form['email']
    try:
        auth.send_password_reset_email(email)
        return redirect('/login')
    except:
        return render_template('forgot.html', message="Email not found")


if __name__ == '__main__':
    app.run(debug=True)