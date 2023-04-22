import pyrebase
from flask import *
app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {

    "apiKey": "AIzaSyCTxlEh2hIvAftDL50N-C_3k0vsuVwzKTw",
    "authDomain": "price-4e6c7.firebaseapp.com",
    "projectId": "price-4e6c7",
    "storageBucket": "price-4e6c7.appspot.com",
    "messagingSenderId": "362588580889",
    "appId": "1:362588580889:web:9e95b78edbf75eb067ce88",
    "databaseURL":""
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}


@app.route("/")
def intro():
    return render_template("temp.html")

#Login
@app.route("/login")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/index")
def index():
    return render_template("index.html")


#forgot password 
@app.route("/forgot_password" , methods=['GET' , 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        auth.send_password_reset_email(email)
        return render_template('login.html')
    return render_template('forgot_password.html')
    
    
#Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    unsuccessful = 'Please check your credentials'
    successsful = 'Login successful'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('index.html', s=successsful)
        except:
            return render_template('login.html', us=unsuccessful)
    return render_template('login.html') 

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

if __name__ == "__main__":
    app.run()   