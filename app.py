import os
import logging
from flask import Flask, render_template, request, jsonify
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Sample data for search results
search_data = [
    {"title": "Wireless Headphones", "price": 89.99, "reviews": 4.5},
    {"title": "Smartphone Stand", "price": 24.99, "reviews": 4.2},
    {"title": "Smart Watch", "price": 199.99, "reviews": 4.7},
    {"title": "Bluetooth Speaker", "price": 59.99, "reviews": 4.3},
    {"title": "Ergonomic Keyboard", "price": 129.99, "reviews": 4.4},
    {"title": "External SSD Drive", "price": 149.99, "reviews": 4.6},
    {"title": "Wireless Mouse", "price": 39.99, "reviews": 4.1},
    {"title": "Laptop Cooling Pad", "price": 29.99, "reviews": 3.9},
    {"title": "USB-C Hub", "price": 45.99, "reviews": 4.0},
    {"title": "Mechanical Keyboard", "price": 89.99, "reviews": 4.8},
    {"title": "Noise Cancelling Earbuds", "price": 159.99, "reviews": 4.5},
    {"title": "Portable Charger", "price": 34.99, "reviews": 4.3}
]


@app.route('/')
def index():
    """Render the main search page."""
    return render_template('index.html')

@app.route('/search')
def search():
    """Handle search requests and return filtered results."""
    query = request.args.get('q', '').lower()
    
    # Filter results based on the search query
    if query:
        results = [item for item in search_data 
                  if query in item['title'].lower()]
    else:
        results = search_data
    
    return render_template('results.html', results=results, query=query)
from program import mainone
@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for search (used for AJAX requests if needed)."""
    query=request.form.get('q')
    results = search_data
    print(query)
    products = mainone(query)
    for product in products:
        print(f"Product:\n{product['title']}\nprice:\n{product['price']}\nReviews:\n{product['reviews']}\n")
    return render_template('results.html', results=products, query=query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
