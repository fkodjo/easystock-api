from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask.json import jsonify

from src.database import Shop, db

shops = Blueprint("shops", __name__, url_prefix="/api/v1/shops")

@shops.route("/", methods=['POST','GET'])
@jwt_required()
def handle_shops():
    current_user = get_jwt_identity()

    if request.method == 'POST':
        wording = request.get_json().get('wording','')
        description = request.get_json().get('description','')

        if not wording:
            return jsonify({
                'error':'Wording not specify'
            },), HTTP_400_BAD_REQUEST
        
        if Shop.query.filter_by(wording=wording).first():
            return jsonify({
                'error':'Wording already exists'
            },), HTTP_409_CONFLICT
        

        shop = Shop(wording=wording, description=description, user_id=current_user)
        db.session.add(shop)
        db.session.commit()

        return jsonify({
            'id': shop.id,
            'wording': shop.wording,
            'description':shop.description,
            'created_at': shop.created_at,
            'update_at': shop.updated_at
        }), HTTP_201_CREATED
    
    else:
        shops = Shop.query.filter_by(user_id=current_user)
        data=[]
        for shop in shops:
            data.append({
                'id': shop.id,
                'wording': shop.wording,
                'description':shop.description,
                'created_at': shop.created_at,
                'update_at': shop.updated_at,
            })

        
        return jsonify({'data':data }), HTTP_200_OK
    
@shops.get("/<int:id>")
@jwt_required()
def get_shop(id):
    current_user = get_jwt_identity()

    shop = Shop.query.filter_by(user_id=current_user, id=id).first()

    if not shop:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    return jsonify({
        'id': shop.id,
        'wording': shop.wording,
        'description':shop.description,
        'created_at': shop.created_at,
        'update_at': shop.updated_at,
    }), HTTP_200_OK


@shops.put('/<int:id>')
@shops.patch('/<int:id>')
@jwt_required()
def edite_shop(id):
    current_user = get_jwt_identity()

    shop = Shop.query.filter_by(use_id=current_user,id=id).first()

    if not shop:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    wording = request.get_json().get('wording','')
    description = request.get_json().get('description','')

    if Shop.query.filter_by(wording=wording).first():

        shop.wording = wording
        shop.description = description
            
        db.session.commit()

        return jsonify({
            'id': shop.id,
            'wording': shop.wording,
            'description':shop.description,
            'created_at': shop.created_at,
            'update_at': shop.updated_at,
        }), HTTP_200_OK
    else:
        return jsonify({'message':'Item not existe'}), HTTP_404_NOT_FOUND

@shops.delete('/<int:id>')
@jwt_required()
def delete_shop(id):
    current_user = get_jwt_identity()

    shop = Shop.query.filter_by(user_id=current_user, id=id).first()

    if not shop:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    db.session.delete(shop)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT