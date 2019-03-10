# app.py
from flask import Flask, request
import json, logging
from flask_restful import Resource, Api, reqparse, marshal
from logging.handlers import RotatingFileHandler
from flask import Blueprint
from . import * #ngambil init.py
from blueprints import app
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_user= Blueprint('user',__name__)
api = Api(bp_user)


class Userresources(Resource):
    @jwt_required
    def get(self, id=None):
        status_admin = get_jwt_claims()['status_admin']
        if status_admin == 'admin':
            if id is None:
                parser = reqparse.RequestParser()
                parser.add_argument('p', type=int, location='args', default = 1)
                parser.add_argument('rp', type=int, location='args', default = 5)
                parser.add_argument('email', location='args')
                parser.add_argument('name', location='args')
                args = parser.parse_args()

                offset = (args['p']*args['rp'])-args['rp']
            
                qry = Users.query
                if args['email'] is not None:
                    qry = qry.filter_by(email=args['email'])
                    qry = qry.filter(Users.email.like("%"+args['email']+"%"))
                if args['name'] is not None:
                    qry = qry.filter_by(name=args['name'])
                    qry = qry.filter(Users.name.like("%"+args['name']+"%"))

                rows = []
                for row in qry.limit(args['rp']).offset(offset).all():
                    rows.append(marshal(row, Users.response_fields))
                return rows, 200, { 'Content-Type': 'application/json' }

            else:
                qry = Users.query.get(id)
                #select *from where id = id
                if qry is not None:
                    return marshal(qry, Users.response_fields), 200, { 'Content-Type': 'application/json' }
                return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
            return {'status':'ACCESS DENIED'}, 404, { 'Content-Type': 'application/json' }

    def post(self,id = None):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        parser.add_argument('name', location='args', required=True)
        parser.add_argument('phone_number', location='args', required=True)
        parser.add_argument('status_admin', location='args', default="user")
        args = parser.parse_args()

        user = Users(None, args['email'], args['password'], args['name'], args['phone_number'], args["status_admin"])
        db.session.add(user)
        db.session.commit()
        return marshal(user, Users.response_fields), 200, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def put(self, id=None):
        user_id = get_jwt_claims()['id']
        qry = Users.query.get(id)
        if user_id == qry.id:
            parser = reqparse.RequestParser()
            parser.add_argument('email', location='args')
            parser.add_argument('password', location='args')
            parser.add_argument('name', location='args')
            parser.add_argument('phone_number', location='args')
            # parser.add_argument('status_admin', location='args', default="user")
            args = parser.parse_args()

            qry = Users.query.get(id)
            if qry is not None:
                qry.email = args['email']
                qry.password = args['password']
                qry.name = args['name']
                qry.phone_number = args['phone_number']
                db.session.commit()
                return marshal(qry, Users.response_fields), 200, { 'Content-Type': 'application/json' }
            return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
           return {'status':'ACCES DENIED', 'message':'INVALID USER'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self, id=None):
        status_admin = get_jwt_claims()['status_admin']
        if status_admin == 'admin':
            qry = Users.query.get(id)
            if qry is not None:
                db.session.delete(qry)
                db.session.commit()
                return "deleted", 200, { 'Content-Type': 'application/json' }
            return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
            return {'status':'ACCES DENIED', 'message':'INVALID ADMIN'}, 404, { 'Content-Type': 'application/json' }

api.add_resource(Userresources,'','/<id>')
