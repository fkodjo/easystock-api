from src.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
import string
from src.database import User, db

auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    phone = request.json['phone']
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    username = phone.replace(" ","")

    if len(password) < 8:
        return jsonify({'error' : 'Password is too short'}), HTTP_400_BAD_REQUEST
    
    if len(username) < 8 :
        return jsonify({'error':'Username is too short'}), HTTP_400_BAD_REQUEST
    
    if " " in username:
        return jsonify({'error':'Username should not contain spaces'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error':'Email is not valid'}), HTTP_409_CONFLICT
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error':'Email is taken'}), HTTP_409_CONFLICT
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error':'username is taken'}), HTTP_409_CONFLICT
    
    pwd_hash = generate_password_hash(password)
    user=User(name=name,username=username,password=pwd_hash,phone=phone,email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message':'user created',
        'user':{
            'name':name,'username':username, 'email':email
        }
    }), HTTP_201_CREATED
    

@auth.post('/login')
def login():
    phone = request.json.get('phone','')
    password = request.json.get('password','')
    username = phone.replace(" ","")

    user = User.query.filter_by(username=username).first()
    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)
            return jsonify({
                'user':{
                    'refresh':refresh,
                    'access':access,
                    'username':user.username,
                    'name': user.name,
                    'phone':user.phone,
                    'email':user.email
                }
            }), HTTP_200_OK
        
    return jsonify({"error":"Wrong credentials"}), HTTP_401_UNAUTHORIZED   

@auth.post('/logout')
def logout():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)


@auth.get('/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        'name': user.name,
        'phone': user.phone,
        'email': user.email,
        'created_at': user.created_at
    }), HTTP_200_OK

    
@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        'access':access
    }), HTTP_200_OK