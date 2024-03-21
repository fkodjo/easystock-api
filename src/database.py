from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
from enum import unique
from sqlalchemy.orm import backref
import random


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(127), unique=True, nullable=True)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    
    shops = db.relationship('Shop', backref="user", lazy=True)
    clients = db.relationship('Client',backref='user', lazy=True)

    def __repr__(self) -> str:
        return 'User>>> {self.phone}'


class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(167), nullable=False)
    phone = db.Column(db.String(14), nullable=True)
    purchases = db.relationship('Purchase', backref="client", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return 'Client>>> {self.name}'


class Shop(db.Model):
    __tablename__ = "shops"
    id = db.Column(db.Integer, primary_key=True)
    wording = db.Column(db.String(167),unique=True,nullable=False)
    description = db.Column(db.Text(),nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())
    categories = db.relationship('Category', backref="shop", lazy=True)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return 'Shop>>> {self.wording}'



class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    wording = db.Column(db.String(167), unique=False, nullable=False)
    description = db.Column(db.Text(),nullable=True)
    products = db.relationship('Product', backref="category", lazy=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate = datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return 'Category>>> {self.wording}'


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    wording = db.Column(db.String(167),unique=False,nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Double, nullable=True)
    quantity = db.Column(db.Integer, default=0)
    expired_at = db.Column(db.DateTime, default=None)
    created_at = db.Column(db.DateTime, default=datetime.now())
    update_at = db.Column(db.DateTime, onupdate=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return 'Product>>> {self.wording}'

class Purchase(db.Model):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    remittance = db.Column(db.Double, nullable=True)
    purchased = db.relationship('Purchased', backref="purchase", lazy=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id')) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return 'Purchase>>> {self.created_at}' 

class Purchased(db.Model):
    __tablename__="purchased"
    id = db.Column(db.Integer, primary_key=True)
    remittance = db.Column(db.Double, nullable=True)
    quantity = db.Column(db.Integer, default=1)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'))
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return 'Purchased>>> {self.product_id}'
    


