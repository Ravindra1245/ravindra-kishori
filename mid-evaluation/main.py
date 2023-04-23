import pyrebase
from flask import *
import requests
from bs4 import BeautifulSoup
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {

    "apiKey": "AIzaSyAHNUwFLMVv91t3ntaXYTCglULRlIg0oJw",
    "authDomain": "pricecompareg28.firebaseapp.com",
    "projectId": "pricecompareg28",
    "storageBucket": "pricecompareg28.appspot.com",
    "messagingSenderId": "30273225015",
    "appId": "1:30273225015:web:efd069b091f2c35dea9ab2",
    "measurementId": "G-FFNVTMBVDV",

    # "apiKey": "AIzaSyCTxlEh2hIvAftDL50N-C_3k0vsuVwzKTw",
    # "authDomain": "price-4e6c7.firebaseapp.com",
    # "projectId": "price-4e6c7",
    # "storageBucket": "price-4e6c7.appspot.com",
    # "messagingSenderId": "362588580889",
    # "appId": "1:362588580889:web:9e95b78edbf75eb067ce88",
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
    
@app.route("/price")
def price():
    return render_template("price.html")

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


@app.route('/search', methods=['POST'])
def search():
    query = request.form['search_box']
    result = execute_search(query)
    return render_template('search.html', result=result)

def execute_search(query):
    name=query
    name1 = name.replace(" ","+")
    google=f'https://www.google.com/search?q={name1}&tbm=shop&sxsrf=GENERATED_STRING&psb=1&ei=GENERATED_STRING&ved=GENERATED_STRING&uact=5&oq={name1}&gs_lcp=Cgtwcm9kdWN0cy1jYxADMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMgcIABCKBRBDMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgQIABADMgsIABCABBCxAxCDAToFCAAQgARQAFjqBmDHB2gAcAB4AIAB0wGIAdgCkgEFMC4xLjGYAQCgAQHAAQE&sclient=products-cc'
    res = requests.get(f'https://www.google.com/search?q={name1}&tbm=shop&sxsrf=GENERATED_STRING&psb=1&ei=GENERATED_STRING&ved=GENERATED_STRING&uact=5&oq={name1}&gs_lcp=Cgtwcm9kdWN0cy1jYxADMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMgcIABCKBRBDMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgQIABADMgsIABCABBCxAxCDAToFCAAQgARQAFjqBmDHB2gAcAB4AIAB0wGIAdgCkgEFMC4xLjGYAQCgAQHAAQE&sclient=products-cc',headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    parent_div = soup.find('div', class_='GhTN2e')
    details = parent_div.find_all('h3', class_='sh-np__product-title translate-content')
    prices = parent_div.find_all('div', class_='KZmu8e')
    sites = parent_div.find_all('span', class_='E5ocAb')
    links = parent_div.find_all('a', class_='sh-np__click-target')
    images = parent_div.find_all('img')
    list = []
 
    def price_to_int(price_str):
        price_str = price_str.replace('₹', '').replace('.', '').replace(',','')
        price_int = int(price_str)
        return price_int


    for [info0, info1, info2, info3, info4] in zip(details, sites , prices, links, images):
        try:
            priceint = price_to_int(info2.b.text)
        except:
            priceint = 0
        
        list.append([int(priceint/100) , info0.text, info1.text, info2.b.text, info3.href, info4['src']])
        #list.append([int(priceint/100) , 0, info1.text, info2.b.text, info3.href])

    list.sort(reverse=True)
    return list



if __name__ == "__main__":
    app.run()   