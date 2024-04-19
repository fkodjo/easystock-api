template = {
    "swagger":"2.0",
    "infos": {
        "title":"Stocks API",
        "description":"Stores and Stocks management API",
        "contact":{
            "responsibleOrganization":"",
            "responsibleDevelopper": "",
            "email":"easystock.tg@gmail.com",
            "url":""
        },
        "termsOfService":"",
        "version": "1.0"
    },
    "basePath": "/api/v1/", # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Exemple: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True, # all in
            "modzl_filter": lambda tag: True, # all in
        },
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}