# app.py
from flask import Flask, request
import json, logging
from flask_restful import Resource, Api, reqparse, marshal
from logging.handlers import RotatingFileHandler
from flask import Blueprint
from . import * #ngambil init.py
from blueprints import app
from blueprints.collection import *
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_cart= Blueprint('cart',__name__)
api = Api(bp_cart)


class cartresources(Resource):
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
            
                qry = carts.query
                if args['email'] is not None:
                    qry = qry.filter_by(email=args['email'])
                    qry = qry.filter(carts.email.like("%"+args['email']+"%"))
                if args['name'] is not None:
                    qry = qry.filter_by(name=args['name'])
                    qry = qry.filter(carts.name.like("%"+args['name']+"%"))

                rows = []
                for row in qry.limit(args['rp']).offset(offset).all():
                    rows.append(marshal(row, carts.response_fields))
                return rows, 200, { 'Content-Type': 'application/json' }

            else:
                qry = carts.query.get(id)
                #select *from where id = id
                if qry is not None:
                    return marshal(qry, carts.response_fields), 200, { 'Content-Type': 'application/json' }
                return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
            return {'status':'ACCESS DENIED'}, 404, { 'Content-Type': 'application/json' }

    def post(self,id = None):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        parser.add_argument('product_id', location='args', required=True)
        parser.add_argument('user_id', location='args', required=True)
        args = parser.parse_args()

        produk = Collections.query.get(args['product_id'])
        products = marshal(produk, Collections.response_fields)
        uuser = Collections.query.get(args['user_id'])
        uusers = marshal(uuser, Collections.response_fields)

        cart = carts(id, args['id'], args['product_id'], args['user_id'], products, uusers)
        db.session.add(cart)
        db.session.commit()
        return marshal(cart, carts.response_fields), 200, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def put(self, id=None):
        cart_id = get_jwt_claims()['id']
        qry = carts.query.get(id)
        if cart_id == qry.id:
            parser = reqparse.RequestParser()
            parser.add_argument('id', location='args')
            parser.add_argument('product_id', location='args')
            parser.add_argument('user_id', location='args')
            args = parser.parse_args()

            qry = carts.query.get(id)
            if qry is not None:
                qry.id = args['id']
                qry.product_id = args['product_id']
                qry.user_id = args['user_id']
                db.session.commit()
                return marshal(qry, carts.response_fields), 200, { 'Content-Type': 'application/json' }
            return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
           return {'status':'ACCES DENIED', 'message':'INVALID cart'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self, id=None):
        status_admin = get_jwt_claims()['status_admin']
        if status_admin == 'user':
            qry = carts.query.get(id)
            if qry is not None:
                db.session.delete(qry)
                db.session.commit()
                return "deleted", 200, { 'Content-Type': 'application/json' }
            return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
            return {'status':'ACCES DENIED', 'message':'INVALID ADMIN'}, 404, { 'Content-Type': 'application/json' }

api.add_resource(cartresources,'','/<id>')
