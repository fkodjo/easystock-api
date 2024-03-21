from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask.json import jsonify
import validators

from src.database import Client, User, Purchase, db

clients = Blueprint("clients",__name__,url_prefix="/api/v1/cliens")

@clients.route("/", methods=['POST','GET'])
@jwt_required()
def handle_clients():

    current_user = get_jwt_identity()

    if request.method == 'POST':
        name = request.get_json().get('name','')
        phone = request.get_json().get('phone','')

        if not name:
            return jsonify({'error':'client name not specify'})
        if not phone:
            return jsonify({'error':'Phone number not defined'})
        if not User.query._filter_by(id=current_user).first():
            return jsonify({'error':'User not exists'})

        client = Client(name=name,phone=phone,user_id=current_user)
        db.session.add(client)
        db.session.commit()

        return jsonify({
            'id': client.id,
            'name': client.name,
            'phone':client.phone,
            'user_id':client.user_id
        }), HTTP_201_CREATED
    

@clients.get("/<int:id>")
@jwt_required()
def get_clients(id):

    current_user = get_jwt_identity()

    client = Client.query.filter_by(id=id,user_id=current_user).first()

    if not client:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    purchases = Purchase.query.filter_by(client_id=id)
    list_purchases = []

    if purchases:
        for item in purchases:
            list_purchases.append(item)

    
    return jsonify({
        'id': client.id,
        'name': client.name,
        'phone':client.phone,
        'purchases':list_purchases,
        'user_id':client.user_id
        }), HTTP_200_OK


@clients.put('/<int:id>')
@clients.patch('/<int:id>')
@jwt_required()
def edite_clients(id):

    current_user = get_jwt_identity()

    client = Client.query.filter_by(id=id).first()

    if not client:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    client.name = request.get_json().get('remittance','')
    client.phone = request.get_json().get('quantity','')
    client.user_id = current_user

            
    db.session.commit()

    return jsonify({
        'id': client.id,
        'name': client.name,
        'phone':client.phone,
        'user_id':client.user_id
        }), HTTP_200_OK

@clients.delete('/<int:id>')
@jwt_required()
def delete_clients(id):

    client = Client.query.filter_by(id=id).first()

    if not client:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    db.session.delete(client)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT