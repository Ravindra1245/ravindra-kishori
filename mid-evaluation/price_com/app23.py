from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import pyrebase
from flask import Flask, render_template, redirect
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Start the Chrome browser
driver = webdriver.Chrome()

# Go to the Flipkart website
driver.get("https://www.flipkart.com/")

# Find the search box and enter the product name
search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
search_box.send_keys("laptops")
search_box.send_keys(Keys.RETURN)

# Wait for the page to load
driver.implicitly_wait(10)

html = driver.page_source
# Get the page source using BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

flipkart_products = {}

for product in soup.find_all('div', {'class': '_2kHMtA'}):
    product_name = product.find('div', {'class': '_4rR01T'}).text.strip()
    product_price = product.find('div', {'class': '_30jeq3 _1_WHN1'}).text.strip()
    product_url = 'https://www.flipkart.com' + product.find('a', {'class': '_1fQZEK'}).get('href')
    product_id = product_url.split("/")[3]
    
    # Check if product image is present
    product_image = product.find('img', {'class': '_396cs4 _3exPp9'})
    if product_image is not None:
        product_image_url = product_image.get('src')
    else:
        product_image_url = ''
    
    data = {"product_id": product_id,
            "product_name": product_name,
            "product_price": product_price,
            "product_image_url": product_image_url,
            "product_url": product_url}
    db.child("flipkart_products").child(product_id).set(data)

# Scrape data from Amazon
amazon_url = "https://www.amazon.com/s?k=laptop"
amazon_response = requests.get(amazon_url)
amazon_soup = BeautifulSoup(amazon_response.content, "html.parser")
amazon_products = amazon_soup.find_all("div", {"data-component-type": "s-search-result"})

# Store the data in Firebase
for product in amazon_products:
    product_name = product.find("h2").text.strip()
    product_price = product.find("span", {"class": "a-price-whole"}).text.strip()
    product_image_url = product.find("img")['src']
    data = {"product_name": product_name, "product_price": product_price, "product_image_url": product_image_url}
    db.child("amazon_products").push(data)

# Create a Flask app








app = Flask(__name__)

@app.route("/")
def home():
    # Retrieve the data from Firebase
    amazon_products = db.child("amazon_products").get().val()
    flipkart_products = db.child("flipkart_products").get().val()
    return render_template("index.html", amazon_products=amazon_products, flipkart_products=flipkart_products)

@app.route("/product/<id>")
def product(id):
    # Retrieve the data for the product with the given ID from Firebase
    product_data = db.child("flipkart_products").child(id).get().val()

    # Redirect the user to the product page on Flipkart
    return redirect(product_data["product_url"])

if __name__ == "__main__":
    app.run(debug=True)
