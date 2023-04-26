import pyrebase
from flask import *
import requests
from bs4 import BeautifulSoup
import random
from collections import *
import re

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

global lists
global rated_lists
global my_dict
global rated_my_dict


app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {

    "apiKey": "AIzaSyAHNUwFLMVv91t3ntaXYTCglULRlIg0oJw",
    "authDomain": "pricecompareg28.firebaseapp.com",
    "databaseURL": "https://pricecompareg28-default-rtdb.firebaseio.com/" ,
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
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}
ekey ="" #key to store in database

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

@app.route("/search_history" , methods=['GET'])
def search_history():
    his = db.child(ekey).get().val()
    if his is None :
        return render_template("no_search_history.html")
    else:
        history_names=[]
        his = list(his.values())
        for i in his:
            history_names.append(i['History'])
        return render_template("search_history.html" , history_names=history_names)

@app.route("/no_search_history" , methods=['GET'])
def no_search_history():
    db.child(ekey).remove()
    return render_template("no_search_history.html")

#forgot password 
@app.route("/forgot_password" , methods=["POST", "GET"])
def forgot_password():
    if request.method == "POST":
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
@app.route("/result", methods = ["POST"])
def result():
    unsuccessful = 'Please check your credentials'
    successsful = 'Login successful'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        global ekey
        ekey = email[:email.index("@")]
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template('index.html', s=successsful)
        except:
            return render_template('login.html', us=unsuccessful)
    return render_template('login.html') 

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        ekey = email[:email.index("@")]
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


@app.route('/search', methods=["POST"])
def search():
    query = request.form['search_box']
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
     
    # Pass the string in search
    # method of regex object.   
    if(regex.search(query) != None):
        # print("Hello")
        err = "Please enter a valid product name"
        return render_template('index.html', err = err)
   
    data = {'History' : query}
    db.child(ekey).push(data)
    result, ans = execute_search(query)
    if ans=="rate":
        return render_template('rated.html', result=result)
    return render_template('search.html', result=result)


def execute_search(query):
    global lists
    global rated_lists
    global my_dict
    global rated_my_dict

    name=query
    name1 = name.replace(" ","+")

    lists = []
    rated_lists=[]
    my_dict = defaultdict(list)
    rated_my_dict = defaultdict(list)

    rep_img=[]
    link = {}

    link["Amazon.in"] = "https://www.amazon.in"
    link["Croma"] = "https://www.croma.com"
    link["Vijay Sales"] = "https://www.vijaysales.com/"
    link["Unicorn Store"] = "https://shop.unicornstore.in/"
    link["Apple"]="https://www.apple.com/in/"
    link["bigbasket.com"]="https://www.bigbasket.com"
    link["Gadgets Now"]="https://shop.gadgetsnow.com/"
    link["Ovantica.com"]="https://ovantica.com/"
    
    google=f'https://www.google.com/search?q={name1}&tbm=shop&sxsrf=GENERATED_STRING&psb=1&ei=GENERATED_STRING&ved=GENERATED_STRING&uact=5&oq={name1}&gs_lcp=Cgtwcm9kdWN0cy1jYxADMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMgcIABCKBRBDMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgQIABADMgsIABCABBCxAxCDAToFCAAQgARQAFjqBmDHB2gAcAB4AIAB0wGIAdgCkgEFMC4xLjGYAQCgAQHAAQE&sclient=products-cc'
    res = requests.get(f'https://www.google.com/search?q={name1}&tbm=shop&sxsrf=GENERATED_STRING&psb=1&ei=GENERATED_STRING&ved=GENERATED_STRING&uact=5&oq={name1}&gs_lcp=Cgtwcm9kdWN0cy1jYxADMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMgcIABCKBRBDMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgQIABADMgsIABCABBCxAxCDAToFCAAQgARQAFjqBmDHB2gAcAB4AIAB0wGIAdgCkgEFMC4xLjGYAQCgAQHAAQE&sclient=products-cc',headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    parent_div = soup.find('div', class_='GhTN2e')
    try:
        details = parent_div.find_all('h3', class_='sh-np__product-title translate-content')
        prices = parent_div.find_all('div', class_='KZmu8e')
        sites = parent_div.find_all('span', class_='E5ocAb')
        links = parent_div.find_all('a', class_='sh-np__click-target')
        images = parent_div.find_all('img')
    except:
        s=0
    try:
        rate_details = soup.find_all('h3', class_='tAxDx')
        rate_ratings = soup.find_all('span', class_='QIrs8')
        rate_prices = soup.find_all('span', class_='a8Pemb OFFNJ')
        rate_sites = soup.find_all('div', class_='aULzUe IuHnof') 
    except:
        return rated_lists, "unrate"

    
    def price_to_int(price_str):
        price_str = price_str.replace('₹', '').replace('.', '').replace(',','')
        price_int = int(price_str)
        return price_int

    try:
        for [info0, info1, info2, info3, info4] in zip(details, sites , prices, links, images):
            try:
                priceint = price_to_int(info2.b.text)
            except:
                priceint = 0
            try:
                img = str(info4['src'])
                if(img=="data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="):
                    n=len(rep_img)
                    random_int = random.randint(0, n-1)
                    img = rep_img[random_int]                
                else:
                    rep_img.append(img)
                site = info1.text
                url="Hello"
                if link[site]:
                    url = link[site]
                else:
                    url = info3['href']
            except:
                x=0
            my_dict[site].append([int(priceint/100) , info0.text, info1.text, info2.b.text, url, img])
            lists.append([int(priceint/100) , info0.text, info1.text, info2.b.text, url, img])
    except:
        s=0
    try:
        for [info0, info1, info2, info3] in zip(rate_details, rate_ratings , rate_prices, rate_sites):
            try:
                priceint = price_to_int(info2.text)
                site = info3.text
            except:
                priceint = 0
            rated_my_dict[site].append([int(priceint/100) , info0.text, info1.text, info2.text, info3.text])
            rated_lists.append([int(priceint/100) , info0.text, info1.text, info2.text, info3.text])
    except:
        s=0

    if len(lists)==0:
        return rated_lists, "rate"
    return lists,"unrate"

@app.route('/sorted', methods=["POST"])
def sorted():
    
    global lists
    global my_dict
    global rated_lists
    global rated_my_dict

    rate_type = request.form['rate']
    sorttype = request.form['price'] 
    company = request.form['Filter-box']
    print(rate_type)
    print(sorttype) 
    print(company)

    st=[]

    if rate_type == "rated" or len(lists)==0:
        
        if company == "" or company in rated_my_dict:
            if company!="":
                st = rated_my_dict[company]
            else:
                st = rated_lists

            if sorttype=="asc":
                st.sort()
            elif sorttype=="desc": 
                st.sort(reverse=True)
            return render_template('rated.html', result=st)
        else:
            return render_template('search.html', us="Please enter valid Store")


    elif rate_type == "unrated":

        if company == "" or company in my_dict:
            if company!="":
                st = my_dict[company]
            else:
                st = lists

            if sorttype=="asc":
                st.sort()
            elif sorttype=="desc": 
                st.sort(reverse=True)
            return render_template('search.html', result=st)
        else:
            return render_template('search.html', us="Please enter valid Store")



   

@app.route('/compare', methods=["POST"])
def compare():
    if len(lists)==0:
        return render_template('search.html') 
    global my_dict
    unsuc="Please Enter Valid Stores"
    try:
        store1 = request.form['store1']
        store2 = request.form['store2']
    except:
        return render_template('search.html', us=unsuc)
    
    if store1=="" or store2=="":
        return render_template('search.html', us=unsuc) 
    
    list1 = my_dict[store1]
    list2 = my_dict[store2]
    if len(list1)==0 or len(list2)==0 or store1 == store2:
        return render_template('search.html', us = "No Such Comparision Possible") 

    list1.sort()
    list2.sort()
    Compresult = [] 
    Compresult.append(list1[0])
    Compresult.append(list2[0])
    return render_template('search.html', result=Compresult)

# @app.route('/rated', methods = ["POST"])
# def rated():
#     global rated_lists
#     return render_template('rated.html', result=rated_lists)



if __name__ == "__main__":
    app.run()   


    