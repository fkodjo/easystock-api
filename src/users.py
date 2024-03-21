from flask_jwt_extended.view_decorators import jwt_required
from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from flask.json import jsonify
import validators

from src.database import db, User

users = Blueprint("users",__name__,url_prefix="/api/v1/users")

@users.route('/',methods = ['POST','GET'])
def edit_user(id):
    current_user = get_jwt_identity()

    user = User.query.filter_by(user_id=current_user,id=id).first()

    if not user:
        return jsonify({'message':'Item not found'},), HTTP_404_NOT_FOUND
    
    