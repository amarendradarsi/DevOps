from flask import Flask, render_template
from pymongo import MongoClient
import urllib.parse
from dotenv import load_dotenv  
import os  

load_dotenv()

app = Flask(__name__)

MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

encoded_password = urllib.parse.quote(MONGODB_PASSWORD)


client = None
db = None
products_collection = None

try:
    
    client = MongoClient(f'mongodb+srv://{MONGODB_USERNAME}:{encoded_password}@devops.agzoj.mongodb.net/shop_db?retryWrites=true&w=majority')
    
    db = client['shop_db']
    products_collection = db['products']  
    print("Connected to MongoDB successfully")

except Exception as e:
    print("Could not connect to MongoDB:", e)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
   
    if products_collection is None:
        return "Error: MongoDB connection not established.", 500

    try:
        products_list = list(products_collection.find({}))  
        return render_template('products.html', products=products_list)
    except Exception as e:
        print("Error fetching products:", e)
        return render_template('products.html', products=[])

if __name__ == '__main__':
    app.run(debug=True)
