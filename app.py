import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
import numpy as np
from PIL import Image
import io
import base64

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///products.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Import product recognition and database after app initialization
from product_recognition import classify_product, load_model
from product_database import get_product_by_name, get_alternative_products

with app.app_context():
    # Import models
    import models
    db.create_all()
    
    # Load the model
    load_model()
    
    # Initialize the database with sample data
    from product_database import initialize_database
    initialize_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search/results', methods=['POST'])
def search_results():
    product_name = request.form.get('product_name', '').strip()
    
    if not product_name:
        flash('Please enter a product name', 'warning')
        return redirect(url_for('search'))
    
    try:
        # Get the product from the database
        product = get_product_by_name(product_name)
        
        if product:
            # Get alternative products
            alternatives = get_alternative_products(product)
            return render_template('result.html', product=product, alternatives=alternatives)
        else:
            flash('Product not found. Please try another product name.', 'warning')
            return redirect(url_for('search'))
    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        flash('An error occurred while searching. Please try again.', 'danger')
        return redirect(url_for('search'))

@app.route('/scan/results', methods=['POST'])
def scan_results():
    try:
        # Get the image data from the request
        image_data = request.form.get('image')
        
        if not image_data:
            flash('No image provided', 'warning')
            return redirect(url_for('scan'))
        
        # Remove the data URL prefix
        image_data = image_data.replace('data:image/jpeg;base64,', '')
        
        # Convert base64 string to image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Classify the product
        product_name = classify_product(image)
        
        if product_name:
            # Get the product from the database
            product = get_product_by_name(product_name)
            
            if product:
                # Get alternative products
                alternatives = get_alternative_products(product)
                return render_template('result.html', product=product, alternatives=alternatives)
            else:
                flash('Product recognized but not found in database.', 'warning')
                return redirect(url_for('scan'))
        else:
            flash('Could not recognize any product in the image. Please try again.', 'warning')
            return redirect(url_for('scan'))
    except Exception as e:
        logger.error(f"Error in scan: {str(e)}")
        flash('An error occurred while scanning. Please try again.', 'danger')
        return redirect(url_for('scan'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
