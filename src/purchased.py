from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask.json import jsonify

from src.database import Purchased, Purchase, db

bpurchased = Blueprint("bpurchased", __name__, url_prefix="/api/v1/purchased")

@bpurchased.route("/", methods=['POST','GET'])
@jwt_required()
def handle_bpurchased():

    if request.method == 'POST':
        remittance = request.get_json().get('remittance','')
        quantity = request.get_json().get('quantity','')
        product_id = request.get_json().get('product_id','')
        purchase_id = request.get_json().get('purchase_id','')

        if not purchase_id:
            return jsonify({
                'error':'purchase not initiated'
            }), HTTP_400_BAD_REQUEST
        
        if not product_id:
            return jsonify({
                'error':'Product not provided'
            }), HTTP_400_BAD_REQUEST
        
        if not Purchase.query.filter_by(purchase_id=purchase_id).first():
            return jsonify({
                'error':'Purchase not exists'
            }), HTTP_404_NOT_FOUND
        

        purchased = Purchased(remittance=remittance,product_id=product_id,purchase_id=purchase_id,quantity=quantity)
        db.session.add(purchased)
        db.session.commit()

        return jsonify({
            'id': purchased.id,
            'remittance': purchased.remittance,
            'purchase_id':purchased.purchase_id,
            'product_id': purchased.product_id,
            'quantity':purchased.quantity
        }), HTTP_201_CREATED
    

@bpurchased.get("/<int:id>")
@jwt_required()
def get_bpurchased(id):

    purchased = Purchased.query.filter_by(id=id).first()

    if not purchased:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    return jsonify({
        'id': purchased.id,
        'remittance': purchased.remittance,
        'purchase_id':purchased.purchase_id,
        'product_id': purchased.product_id,
        'quantity':purchased.quantity
        }), HTTP_200_OK


@bpurchased.put('/<int:id>')
@bpurchased.patch('/<int:id>')
@jwt_required()
def edite_bpurchased(id):

    purchased = Purchased.query.filter_by(id=id).first()

    if not purchased:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    purchased.remittance = request.get_json().get('remittance','')
    purchased.quantity = request.get_json().get('quantity','')
    purchased.product_id = request.get_json().get('product_id','')
    purchased.purchase_id = request.get_json().get('purchase_id','')

            
    db.session.commit()

    return jsonify({
        'id': purchased.id,
        'remittance': purchased.remittance,
        'purchase_id':purchased.purchase_id,
        'product_id': purchased.product_id,
        'quantity':purchased.quantity
        }), HTTP_200_OK

@bpurchased.delete('/<int:id>')
@jwt_required()
def delete_bpurchased(id):

    purchased = Purchased.query.filter_by(id=id).first()

    if not purchased:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    db.session.delete(purchased)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT