import logging
from models import Product
from app import db

logger = logging.getLogger(__name__)

# Sample data for the database
# In a real application, this would be loaded from a database
SAMPLE_PRODUCTS = [
    # American products
    {"name": "Coca-Cola", "brand": "The Coca-Cola Company", "category": "Beverage", "is_american": True,
     "description": "Carbonated soft drink manufactured by The Coca-Cola Company.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/drink/1F964.svg"},
    
    {"name": "Pepsi", "brand": "PepsiCo", "category": "Beverage", "is_american": True,
     "description": "Carbonated soft drink manufactured by PepsiCo.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/drink/1F964.svg"},
    
    {"name": "Dr Pepper", "brand": "Keurig Dr Pepper", "category": "Beverage", "is_american": True,
     "description": "Carbonated soft drink marketed as having a unique flavor.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/drink/1F964.svg"},
    
    {"name": "Mountain Dew", "brand": "PepsiCo", "category": "Beverage", "is_american": True,
     "description": "Citrus-flavored soft drink produced by PepsiCo.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/drink/1F964.svg"},
    
    {"name": "Doritos", "brand": "Frito-Lay", "category": "Snack", "is_american": True,
     "description": "Flavored tortilla chips produced by Frito-Lay.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35F.svg"},
    
    {"name": "Lay's", "brand": "Frito-Lay", "category": "Snack", "is_american": True,
     "description": "Potato chip brand produced by Frito-Lay.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35F.svg"},
    
    {"name": "Cheetos", "brand": "Frito-Lay", "category": "Snack", "is_american": True,
     "description": "Cheese-flavored, puffed cornmeal snacks made by Frito-Lay.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35F.svg"},
    
    {"name": "Oreo", "brand": "Nabisco", "category": "Snack", "is_american": True,
     "description": "Sandwich cookie consisting of two chocolate wafers with a sweet cream filling.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-sweet/1F36A.svg"},
    
    {"name": "Hershey's", "brand": "The Hershey Company", "category": "Chocolate", "is_american": True,
     "description": "Chocolate bar manufactured by The Hershey Company.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-sweet/1F36B.svg"},
    
    {"name": "Reese's", "brand": "The Hershey Company", "category": "Chocolate", "is_american": True,
     "description": "Chocolate cup filled with peanut butter.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-sweet/1F36B.svg"},
    
    {"name": "Campbell's Soup", "brand": "Campbell Soup Company", "category": "Food", "is_american": True,
     "description": "Canned soup and related products.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F372.svg"},
    
    {"name": "Heinz Ketchup", "brand": "Kraft Heinz", "category": "Condiment", "is_american": True,
     "description": "Tomato ketchup brand.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F957.svg"},
    
    {"name": "Kraft Mac & Cheese", "brand": "Kraft Foods", "category": "Food", "is_american": True,
     "description": "Packaged macaroni and cheese product.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35C.svg"},
    
    {"name": "Cheerios", "brand": "General Mills", "category": "Cereal", "is_american": True,
     "description": "Brand of cereal manufactured by General Mills.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35E.svg"},
    
    {"name": "Lucky Charms", "brand": "General Mills", "category": "Cereal", "is_american": True,
     "description": "Brand of cereal with marshmallow pieces.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35E.svg"},
    
    # Non-American alternatives
    {"name": "Fanta", "brand": "The Coca-Cola Company", "category": "Beverage", "is_american": False,
     "description": "Fruit-flavored carbonated soft drink created in Germany.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/drink/1F964.svg"},
    
    {"name": "Mirinda", "brand": "PepsiCo", "category": "Beverage", "is_american": False,
     "description": "A brand of soft drink originally created in Spain, now owned by PepsiCo.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/drink/1F964.svg"},
    
    {"name": "Orangina", "brand": "Suntory", "category": "Beverage", "is_american": False,
     "description": "Carbonated citrus beverage. Originally made in France.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/drink/1F964.svg"},
    
    {"name": "Inca Kola", "brand": "The Coca-Cola Company", "category": "Beverage", "is_american": False,
     "description": "Sweet, fruity-flavored soft drink from Peru.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/drink/1F964.svg"},
    
    {"name": "Pringles", "brand": "Kellogg's", "category": "Snack", "is_american": False,
     "description": "Brand of potato and wheat-based stackable snack chips. Though American in origin, now produced by Kellogg's which has significant international operations.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35F.svg"},
    
    {"name": "Walkers", "brand": "PepsiCo", "category": "Snack", "is_american": False,
     "description": "British snack food manufacturer primarily known for potato crisps.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35F.svg"},
    
    {"name": "Takis", "brand": "Barcel", "category": "Snack", "is_american": False,
     "description": "Mexican brand of rolled corn tortilla chip snack made by Barcel.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35F.svg"},
    
    {"name": "Chokis", "brand": "Gamesa", "category": "Snack", "is_american": False,
     "description": "Mexican chocolate chip cookie brand.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-sweet/1F36A.svg"},
    
    {"name": "Cadbury", "brand": "Mondelez International", "category": "Chocolate", "is_american": False,
     "description": "British multinational confectionery company.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-sweet/1F36B.svg"},
    
    {"name": "Kinder", "brand": "Ferrero", "category": "Chocolate", "is_american": False,
     "description": "Italian brand of chocolate produced by Ferrero.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-sweet/1F36B.svg"},
    
    {"name": "Knorr Soup", "brand": "Unilever", "category": "Food", "is_american": False,
     "description": "German food and beverage brand owned by Unilever.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F372.svg"},
    
    {"name": "HP Sauce", "brand": "Heinz", "category": "Condiment", "is_american": False,
     "description": "British brown sauce, now owned by Heinz.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F957.svg"},
    
    {"name": "Barilla Pasta", "brand": "Barilla Group", "category": "Food", "is_american": False,
     "description": "Italian pasta brand.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35C.svg"},
    
    {"name": "Weetabix", "brand": "Weetabix Limited", "category": "Cereal", "is_american": False,
     "description": "British breakfast cereal.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35E.svg"},
    
    {"name": "Nestlé Cereal", "brand": "Nestlé", "category": "Cereal", "is_american": False,
     "description": "Swiss multinational food and drink processing corporation.", 
     "image_url": "https://cdn.jsdelivr.net/npm/@svgmoji/openmoji@2.0.0/svg/food-drink/food-prepared/1F35E.svg"}
]

def initialize_database():
    """
    Initialize the database with sample data if it's empty.
    """
    try:
        # Check if the database is empty
        if Product.query.count() == 0:
            for product_data in SAMPLE_PRODUCTS:
                product = Product(**product_data)
                db.session.add(product)
            
            db.session.commit()
            logger.info("Database initialized with sample products")
        else:
            logger.info("Database already contains products. Skipping initialization.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error initializing database: {str(e)}")

def get_product_by_name(name):
    """
    Get a product by name.
    
    Args:
        name: Product name to search for
        
    Returns:
        Product object or None if not found
    """
    try:
        # Try to find an exact match
        product = Product.query.filter(Product.name == name).first()
        
        # If no exact match, try a case-insensitive search
        if not product:
            product = Product.query.filter(Product.name.ilike(f'%{name}%')).first()
        
        return product.to_dict() if product else None
    except Exception as e:
        logger.error(f"Error getting product by name: {str(e)}")
        return None

def get_alternative_products(product, limit=3):
    """
    Get alternative non-American products for a given American product.
    
    Args:
        product: Product dict object
        limit: Maximum number of alternatives to return
        
    Returns:
        List of alternative Product objects
    """
    try:
        if not product.get('is_american', True):
            # If the product is already non-American, return similar products
            alternatives = Product.query.filter(
                Product.category == product['category'],
                Product.id != product['id'],
                Product.is_american == False
            ).limit(limit).all()
        else:
            # If the product is American, find non-American alternatives
            alternatives = Product.query.filter(
                Product.category == product['category'],
                Product.is_american == False
            ).limit(limit).all()
        
        return [alt.to_dict() for alt in alternatives] if alternatives else []
    except Exception as e:
        logger.error(f"Error getting alternative products: {str(e)}")
        return []

# We'll initialize the database from app.py instead to avoid circular imports
# The app.py file will call initialize_database() after creating the app context
