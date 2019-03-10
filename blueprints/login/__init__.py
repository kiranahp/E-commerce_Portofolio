import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from .. import db
from blueprints.user import Users
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_login = Blueprint('login', __name__)
api = Api(bp_login)

class CreateTokenResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location = 'args', required = True)
        parser.add_argument('password', location = 'args', required = True)
        args = parser.parse_args()

        qry = Users.query.filter_by(email = args['email']).filter_by(password = args['password']).first()


        if qry is not None:
            token = create_access_token(identity = marshal(qry, Users.response_fields))
        else:
            return {'status': 'UNAUTORIZED', 'message': 'Invalid key or secret'}, 401
        return {'token' : token}, 200

api.add_resource(CreateTokenResource, '')