from flask import Flask
import os
from src.auth import auth
from src.database import db, Shop, Category
from src.shops import shops
from src.categories import categories
from src.products import products
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY="SECRET_KEY",
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            #SECRET_KEY=os.environ.get("SECRET_KEY"),
            #SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            #SQLALCHEMY_TRACK_MODIFICATIONS=False,
            #JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),

            SWAGGER={
                'title':"Stocks API",
                'uiversion': 3
            }
        )

    else:
        app.config.from_mapping(test_config)

    db.app=app
    db.init_app(app)
    with app.app_context():
        db.create_all()

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(shops)
    app.register_blueprint(categories)

    Swagger(app,config=swagger_config,template=template)
    
    return app