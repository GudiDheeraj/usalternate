from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    is_american = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'category': self.category,
            'is_american': self.is_american,
            'description': self.description,
            'image_url': self.image_url
        }
