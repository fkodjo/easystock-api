from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask.json import jsonify
import validators

from src.database import Purchase, Purchased, db

purchases = Blueprint("purchases", __name__, url_prefix="/api/v1/purchased")

@purchases.route("/", methods=['POST','GET'])
@jwt_required()
def handle_purchases():

    if request.method == 'POST':
        remittance = request.get_json().get('remittance','')
        client_id = request.get_json().get('client_id')

        if not remittance:
            remittance = 0

        if not client_id:
            return jsonify({'error':'client not specified'})

        purchase = Purchase(remittance=remittance,client_id=client_id)
        db.session.add(purchase)
        db.session.commit()

        return jsonify({
            'id': purchase.id,
            'remittance': purchase.remittance,
            'client_id':purchase.client_id
        }), HTTP_201_CREATED
    

@purchases.get("/<int:id>")
@jwt_required()
def get_purchases(id):

    purchase = Purchase.query.filter_by(id=id).first()

    purchased = Purchased.query.filter_by(purchase_id=id).first()

    list_purchased = []

    if not purchase:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    if purchased:
        for item in purchased:
            list_purchased.append(item)

    
    return jsonify({
        'id': purchase.id,
        'remittance': purchase.remittance,
        'purchase_id':purchase.purchase_id,
        'product_id': purchase.product_id,
        'client_id':purchase.client_id,
        'purchases':list_purchased,
        'quantity':purchase.quantity
        }), HTTP_200_OK


@purchases.put('/<int:id>')
@purchases.patch('/<int:id>')
@jwt_required()
def edite_purchases(id):

    purchase = Purchased.query.filter_by(id=id).first()

    if not purchase:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    purchase.remittance = request.get_json().get('remittance','')
    purchase.client_id = request.get_json().get('client_id','')

            
    db.session.commit()

    return jsonify({
        'id': purchase.id,
        'remittance': purchase.remittance,
        'purchase_id':purchase.purchase_id,
        'product_id': purchase.product_id,
        'client_id':purchase.client_id,
        'quantity':purchase.quantity
        }), HTTP_200_OK

purchases.delete('/<int:id>')
@jwt_required()
def delete_purchases(id):

    purchase = Purchase.query.filter_by(id=id).first()

    if not purchase:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    db.session.delete(purchase)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT