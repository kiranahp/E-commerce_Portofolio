import json, sys
from flask import Flask, request, Blueprint
from flask_restful import Resource, Api, reqparse #, abort
from time import strftime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

app.config['APP_DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1:3306/la_quinne'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'NSniSjOIJoijSIjaosJOas'
app.config['JWI_ACCESS_TOKEN_EXPIRES'] = timedelta(days = 1)

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity


db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


api = Api(app, catch_all_404s=True) #using Api-package from restful



@app.after_request # LOG BISA DILIAT DI TERMINAL!!!!
def after_request(response):
    if request.method == 'GET':
        app.logger.warning("REQUEST_LOG\t%s %s",
            response.status_code,
            request.method,
            json.dumps({ 
            'request': request.args.to_dict(), 
            'response': json.loads(response.data.decode('utf-8'))
            }))
    else:
        app.logger.warning("REQUEST_LOG\t%s - %s",
            response.status_code,
            request.method,
            json.dumps({
            'request': request.get_json(),
            'response': json.loads(response.data.decode('utf-8'))
            }))
    return response


# from folder.subfolder.namafile import 
from blueprints.user.resources import bp_user
from blueprints.login import bp_login
from blueprints.collection.resources import bp_collection
from blueprints.payment.resources import bp_payment

app.register_blueprint(bp_user, url_prefix = '/user')
app.register_blueprint(bp_login, url_prefix = '/login')
app.register_blueprint(bp_collection)
app.register_blueprint(bp_payment, url_prefix = '/payment')


db.create_all()
