import requests
from bs4 import BeautifulSoup


headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
name=input("Product Name:\n")

name1 = name.replace(" ","+")

google=f'https://www.google.com/search?q={name1}&tbm=shop&sxsrf=GENERATED_STRING&psb=1&ei=GENERATED_STRING&ved=GENERATED_STRING&uact=5&oq={name1}&gs_lcp=Cgtwcm9kdWN0cy1jYxADMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMgcIABCKBRBDMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgQIABADMgsIABCABBCxAxCDAToFCAAQgARQAFjqBmDHB2gAcAB4AIAB0wGIAdgCkgEFMC4xLjGYAQCgAQHAAQE&sclient=products-cc'
res = requests.get(f'https://www.google.com/search?q={name1}&tbm=shop&sxsrf=GENERATED_STRING&psb=1&ei=GENERATED_STRING&ved=GENERATED_STRING&uact=5&oq={name1}&gs_lcp=Cgtwcm9kdWN0cy1jYxADMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMg0IABCKBRCxAxCDARBDMgcIABCKBRBDMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMgQIABADMgsIABCABBCxAxCDAToFCAAQgARQAFjqBmDHB2gAcAB4AIAB0wGIAdgCkgEFMC4xLjGYAQCgAQHAAQE&sclient=products-cc',headers=headers)

soup = BeautifulSoup(res.text,'html.parser')

parent_div = soup.find('div', class_='GhTN2e')

details = parent_div.find_all('h3', class_='sh-np__product-title translate-content')
prices = parent_div.find_all('div', class_='KZmu8e')
sites = parent_div.find_all('span', class_='E5ocAb')
links = parent_div.find_all('a', class_='sh-np__click-target')

list = []

# for info1 in spans:
#     list.append([info1.text])

# for i in range(len(list)):
#     list[i].append

def price_to_int(price_str):
    # Remove the ₹ currency symbol and decimal point
    price_str = price_str.replace('₹', '').replace('.', '').replace(',','')
    
    # Convert the price string to an integer
    price_int = int(price_str)
    
    return price_int


for [info0, info1, info2, info3] in zip(details, sites , prices, links):
    priceint = price_to_int(info2.b.text)
    list.append([int(priceint/100) , info0.text, info1.text, info2.b.text, info3.href])
    # list.append([int(priceint/100) , 0, info1.text, 0, info3.href])

list.sort(reverse=False)

# print(list)

# for info2 in divs:


for i in list:
    print(i)


