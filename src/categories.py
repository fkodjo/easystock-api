from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask.json import jsonify

from src.database import Category, db

categories = Blueprint("categories", __name__, url_prefix="/api/v1/categories")

@categories.route("/", methods=['POST','GET'])
@jwt_required()
def handle_categories():

    if request.method == 'POST':
        wording = request.get_json().get('wording','')
        description = request.get_json().get('description','')
        shop_id = request.get_json().get('shop_id','')

        if not wording:
            return jsonify({
                'error':'Wording not specify'
                }), HTTP_400_BAD_REQUEST
    
        if not shop_id:
            return jsonify({
                'error':'Shop not specify'
                }), HTTP_400_BAD_REQUEST
    
        if Category.query.filter_by(wording=wording).first():
            return jsonify({
                'error':'Wording already exists'
                }), HTTP_409_CONFLICT
        

        category = Category(wording=wording,description=description,shop_id=shop_id)
        db.session.add(category)
        db.session.commit()

        return jsonify({
            'id': category.id,
            'wording': category.wording,
            'shop_id':category.shop_id,
            'created_at': category.created_at
            }), HTTP_201_CREATED
             
    


@categories.get("/<int:id>")
@jwt_required()
def get_category(id):
    category = Category.query.filter_by(id=id).first()

    if not category:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    return jsonify({
        'id': category.id,
        'wording': category.wording,
        'description':category.description,
        'created_at': category.created_at,
        'update_at': category.updated_at,
        }), HTTP_200_OK


@categories.put('/<int:id>')
@categories.patch('/<int:id>')
@jwt_required()
def edite_category(id):
    category = Category.query.filter_by(id=id).first()

    if not category:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    wording = request.get_json().get('wording','')
    description = request.get_json().get('description','')

    if Category.query.filter_by(wording=wording).first():
        category.wording = wording
        category.description = description
        db.session.commit()

        return jsonify({
            'id': category.id,
            'wording': category.wording,
            'description':category.description,
            'created_at': category.created_at,
            'update_at': category.updated_at,
            }), HTTP_200_OK
    
    else:
        return jsonify({'message':'Item not existe'}), HTTP_404_NOT_FOUND

@categories.delete('/<int:id>')
@jwt_required()
def delete_category(id):

    category = Category.query.filter_by(id=id).first()

    if not category:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    db.session.delete(category)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT