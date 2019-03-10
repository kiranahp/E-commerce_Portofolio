# app.py
from flask import Flask, request
import json, logging
from flask_restful import Resource, Api, reqparse, marshal
from logging.handlers import RotatingFileHandler
from flask import Blueprint
from . import * #ngambil init.py
from blueprints import app
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_payment= Blueprint('payment',__name__)
api = Api(bp_payment)


class paymentresources(Resource):
    @jwt_required
    def get(self, id=None):
        status_admin = get_jwt_claims()['status_admin']
        if status_admin == 'admin':
            if id is None:
                parser = reqparse.RequestParser()
                parser.add_argument('p', type=int, location='args', default = 1)
                parser.add_argument('rp', type=int, location='args', default = 5)
                parser.add_argument('email', location='args')
                parser.add_argument('order_refference', location='args')
                args = parser.parse_args()

                offset = (args['p']*args['rp'])-args['rp']
            
                qry = payments.query
                if args['email'] is not None:
                    qry = qry.filter_by(email=args['email'])
                    qry = qry.filter(payments.email.like("%"+args['email']+"%"))
                if args['order_refference'] is not None:
                    qry = qry.filter_by(order_refference=args['order_refference'])
                    qry = qry.filter(payments.order_refference.like("%"+args['order_refference']+"%"))

                rows = []
                for row in qry.limit(args['rp']).offset(offset).all():
                    rows.append(marshal(row, payments.response_fields))
                return rows, 200, { 'Content-Type': 'application/json' }

            else:
                qry = payments.query.get(id)
                #select *from where id = id
                if qry is not None:
                    return marshal(qry, payments.response_fields), 200, { 'Content-Type': 'application/json' }
                return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
            return {'status':'ACCESS DENIED'}, 404, { 'Content-Type': 'application/json' }

    def post(self,id = None):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='args', required=True)
        parser.add_argument('order_refference',type=int, location='args', required=True)
        parser.add_argument('atas_nama', location='args', required=True)
        parser.add_argument('jumlah_transfer', location='args', required=True)
        parser.add_argument('date_time', location='args', required=True)
        parser.add_argument('bukti_transfer', location='args', required=True)
        parser.add_argument('status', location='args', default='noCheck')
        args = parser.parse_args()

        payment = payments(None, args['email'], args['order_refference'], args['atas_nama'], 
        args['jumlah_transfer'], args["date_time"], args['bukti_transfer'], args['status'])
        db.session.add(payment)
        db.session.commit()
        return marshal(payment, payments.response_fields), 200, { 'Content-Type': 'application/json' }
    
    @jwt_required
    def put(self, id=None):
        status_admin = get_jwt_claims()['status_admin']
        if status_admin == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('email', location='args')
            parser.add_argument('order_refference',type=int, location='args')
            parser.add_argument('atas_nama', location='args')
            parser.add_argument('jumlah_transfer', location='args')
            parser.add_argument('bukti_transfer', location='args')
            parser.add_argument('status', location='args')
            args = parser.parse_args()

            qry = payments.query.get(id)
            if qry is not None:
                qry.email = args['email']
                qry.order_refference = args['order_refference']
                qry.atas_nama = args['atas_nama']
                qry.jumlah_transfer = args['jumlah_transfer']
                qry.jumlah_transfer = args['bukti_transfer']
                qry.status = args['status']
                db.session.commit()
                return marshal(qry, payments.response_fields), 200, { 'Content-Type': 'application/json' }
            return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
           return {'status':'ACCES DENIED', 'message':'INVALID payment'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self, id=None):
        status_admin = get_jwt_claims()['status_admin']
        if status_admin == 'admin':
            qry = payments.query.get(id)
            if qry is not None:
                db.session.delete(qry)
                db.session.commit()
                return "deleted", 200, { 'Content-Type': 'application/json' }
            return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
            return {'status':'ACCES DENIED', 'message':'INVALID ADMIN'}, 404, { 'Content-Type': 'application/json' }

api.add_resource(paymentresources,'','/<id>')
