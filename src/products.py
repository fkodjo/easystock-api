from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask.json import jsonify

from src.database import Product, db

products = Blueprint("products", __name__, url_prefix="/api/v1/products")

@products.route("/", methods=['POST','GET'])
@jwt_required()
def handle_products():

    if request.method == 'POST':
        wording = request.get_json().get('wording','')
        description = request.get_json().get('description','')
        expired_at = request.get_json().get('expired_at','')
        price = request.get_json().get('price','')
        quantity = request.get_json().get('quantity','')
        category_id = request.get_json().get('category_id','')

        if not wording:
            return jsonify({
                'error':'Wording not specify'
            }), HTTP_400_BAD_REQUEST
        
        if not category_id:
            return jsonify({
                'error':'Category not specify'
            }), HTTP_400_BAD_REQUEST
        
        if Product.query.filter_by(wording=wording).first():
            return jsonify({
                'error':'Wording already exists'
            }), HTTP_409_CONFLICT
        

        product = Product(wording=wording,expired_at=expired_at,category_id=category_id,quantity=quantity,price=price,description=description)
        db.session.add(product)
        db.session.commit()

        return jsonify({
            'id': product.id,
            'wording': product.wording,
            'description':product.description,
            'expired_at':product.expired_at,
            'category_id':product.category_id,
            'created_at': product.created_at,
            'quantity':product.quantity,
            'price':product.price
        }), HTTP_201_CREATED
    

@products.get("/<int:id>")
@jwt_required()
def get_product(id):

    product = Product.query.filter_by(id=id).first()

    if not product:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    return jsonify({
        'id': product.id,
        'wording': product.wording,
        'description':product.description,
        'expired_at':product.expired_at,
        'category_id':product.category_id,
        'created_at': product.created_at,
        'updated_at':product.updated_at,
        'quantity':product.quantity,
        'price':product.price
    }), HTTP_200_OK


@products.put('/<int:id>')
@products.patch('/<int:id>')
@jwt_required()
def edite_product(id):

    product = Product.query.filter_by(id=id).first()

    if not product:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    wording = request.get_json().get('wording','')
    description = request.get_json().get('description','')
    expired_at = request.get_json().get('expired_at','')
    category_id = request.get_json().get('category_id','')
    quantity = request.get_json().get('quantity')
    price = request.get_json().get('price','')

    if Product.query.filter_by(wording=wording).first():

        product.wording = wording
        product.description = description
        product.expired_at = expired_at
        product.category_id = category_id
        product.quantity = quantity
        product.price = price
        db.session.commit()

        return jsonify({
            'id': product.id,
            'wording': product.wording,
            'expired_at':product.expired_at,
            'category_id':product.category_id,
            'created_at': product.created_at,
            'quantity':product.quantity,
            'price':product.price
            }), HTTP_200_OK
    else:
        return jsonify({'message':'Item not existe'}), HTTP_404_NOT_FOUND

@products.delete('/<int:id>')
@jwt_required()
def delete_product(id):

    product = Product.query.filter_by(id=id).first()

    if not product:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    db.session.delete(product)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT