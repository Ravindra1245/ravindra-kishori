from bs4 import BeautifulSoup
import requests
import pyrebase
from flask import Flask, render_template

# Firebase configuration
firebaseConfig = {'apiKey': "AIzaSyBmjynphrpL1BTE3dYk01acBctYvtZHGi4",
                  'authDomain': "price-shraddha.firebaseapp.com",
                  'databaseURL': "https://price-shraddha-default-rtdb.firebaseio.com",
                  'projectId': "price-shraddha",
                  'storageBucket': "price-shraddha.appspot.com",
                  'messagingSenderId': "801214337523",
                  'appId': "1:801214337523:web:898bf9b5de63ff8ec44286",
                  'measurementId': "G-HKE64M5DSZ"}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Scrape data from Amazon

# Scrape data from Flipkart
flipkart_url = "https://www.flipkart.com/search?q=ball"
flipkart_response = requests.get(flipkart_url)
flipkart_soup = BeautifulSoup(flipkart_response.content, "html.parser")
flipkart_products = flipkart_soup.find_all("div", {"class": "_2kHMtA"})

# Store the data in Firebase
for product in flipkart_products:
    product_image_url = product.find("img")['src']
    product_name = product.find("div", {"class": "_2WkVRV"}).text.strip()
    product_price = product.find("div", {"class": "_30jeq3 _1_WHN1"}).text.strip()


    
    data = {"product_image_url": product_image_url,"product_name": product_name, "product_price": product_price}
    db.child("flipkart_products").push(data)

# Create a Flask app
app = Flask(__name__)

@app.route("/")
def home():
    # Retrieve the data from Firebase
    
    flipkart_products = db.child("flipkart_products").get().val()
    
    return render_template("index3.html", flipkart_products=flipkart_products)

if __name__ == "__main__":
    app.run(debug=True) 