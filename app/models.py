from app import db
from flask_login import UserMixin  # Importez UserMixin pour faciliter l'intégration avec Flask-Login

class User(UserMixin, db.Model):
    """User"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.id)  # Convertissez l'identifiant en chaîne pour être compatible avec Flask-Login

    def is_authenticated(self):
        return True  # Retournez True si l'utilisateur est authentifié (vous pouvez implémenter une logique plus complexe ici)

    def is_active(self):
        return True  # Retournez True si l'utilisateur est actif (vous pouvez implémenter une logique plus complexe ici)

    def is_anonymous(self):
        return False  # Retournez False car nous avons des utilisateurs authentifiés



class Product(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    generic_name = db.Column(db.String(255))
    brands = db.Column(db.String(255))
    categories = db.Column(db.String(255))
    ingredients_text = db.Column(db.Text)
    labels = db.Column(db.String(255))
    product_name = db.Column(db.String(255))
    quantity = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    proteins = db.Column(db.Float)
    fiber = db.Column(db.Float)
    energy = db.Column(db.Float)
    sugars = db.Column(db.Float)
    saturated_fat = db.Column(db.Float)
    sodium = db.Column(db.Float)

    
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='alerts')
    barcode = db.Column(db.String(100), db.ForeignKey('product.id'))
    description = db.Column(db.Text)





