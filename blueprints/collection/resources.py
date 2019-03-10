# app.py
from flask import Flask, request
import json, logging
from flask_restful import Resource, Api, reqparse, marshal
from logging.handlers import RotatingFileHandler
from flask import Blueprint
from . import * #ngambil init.py
from blueprints import app
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_collection= Blueprint('collection',__name__)
api = Api(bp_collection)


class collectionresources(Resource):
    @jwt_required
    def get(self, id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default = 1)
            parser.add_argument('rp', type=int, location='args', default = 5)
            parser.add_argument('kode_barang', location='args')
            parser.add_argument('label', location='args')
            parser.add_argument('kategori', location='args')
            args = parser.parse_args()

            offset = (args['p']*args['rp'])-args['rp']
        
            qry = Collections.query
            if args['kategori'] is not None:
                qry = qry.filter_by(kategori=args['kategori'])
                qry = qry.filter(Collections.kategori.like("%"+args['kategori']+"%"))
            if args['label'] is not None:
                qry = qry.filter_by(label=args['label'])
                qry = qry.filter(Collections.label.like("%"+args['label']+"%"))
            if args['kode_barang'] is not None:
                qry = qry.filter_by(kode_barang=args['kode_barang'])
                qry = qry.filter(Collections.kode_barang.like("%"+args['kode_barang']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Collections.response_fields))
            return rows, 200, { 'Content-Type': 'application/json' }

        else:
            qry = Collections.query.get(id)
            #select *from where id = id
            if qry is not None:
                return marshal(qry, Collections.response_fields), 200, { 'Content-Type': 'application/json' }
            return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def post(self,id = None):
        status_admin = get_jwt_claims()['status_admin']
        if status_admin == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('kode_barang', location='args', required=True)
            parser.add_argument('harga', location='args', required=True)
            parser.add_argument('deskripsi', location='args', required=True)
            parser.add_argument('label', location='args', default='new')
            parser.add_argument('kategori', location='args', required=True)
            args = parser.parse_args()

            collection = Collections(None, args['kode_barang'],args['harga'], args['deskripsi'], args['label'], args['kategori'])
            db.session.add(collection)
            db.session.commit()
            return marshal(collection, Collections.response_fields), 200, { 'Content-Type': 'application/json' }
        else:
            return {'status':'ACCESS DENIED'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def patch(self, id=None):
        status_admin = get_jwt_claims()['status_admin']
        if status_admin == 'admin':
            parser = reqparse.RequestParser()
            parser.add_argument('kode_barang', location='args')
            parser.add_argument('harga', location='args')
            parser.add_argument('deskripsi', location='args')
            parser.add_argument('label', location='args', default='new')
            parser.add_argument('kategori', location='args')
            args = parser.parse_args()

            qry = Collections.query.get(id)
            if qry is not None:
                qry.kode_barang = args['kode_barang']
                qry.harga = args['harga']
                qry.deskripsi = args['deskripsi']
                qry.label = args['label']
                qry.kategori = args['kategori']
                db.session.commit()
                return marshal(qry, Collections.response_fields), 200, { 'Content-Type': 'application/json' }
            return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
            return {'status':'ACCES DENIED', 'message':'INVALID collection'}, 404, { 'Content-Type': 'application/json' }

    @jwt_required
    def delete(self, id=None):
        status_admin = get_jwt_claims()['status_admin']
        if status_admin == 'admin':
            qry = Collections.query.get(id)
            if qry is not None:
                db.session.delete(qry)
                db.session.commit()
                return "deleted", 200, { 'Content-Type': 'application/json' }
            return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }
        else:
            return {'status':'ACCES DENIED', 'message':'INVALID ADMIN'}, 404, { 'Content-Type': 'application/json' }

class collPublicresources(Resource):
    def get(self, id=None):
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default = 1)
            parser.add_argument('rp', type=int, location='args', default = 5)
            parser.add_argument('kode_barang', location='args')
            parser.add_argument('label', location='args')
            parser.add_argument('kategori', location='args')
            args = parser.parse_args()

            offset = (args['p']*args['rp'])-args['rp']
        
            qry = Collections.query
            if args['kategori'] is not None:
                qry = qry.filter_by(kategori=args['kategori'])
                qry = qry.filter(Collections.kategori.like("%"+args['kategori']+"%"))
            if args['label'] is not None:
                qry = qry.filter_by(label=args['label'])
                qry = qry.filter(Collections.label.like("%"+args['label']+"%"))
            if args['kode_barang'] is not None:
                qry = qry.filter_by(kode_barang=args['kode_barang'])
                qry = qry.filter(Collections.kode_barang.like("%"+args['kode_barang']+"%"))

            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Collections.response_fields))
            return rows, 200, { 'Content-Type': 'application/json' }

        else:
            qry = Collections.query.get(id)
            #select *from where id = id
            if qry is not None:
                return marshal(qry, Collections.response_fields), 200, { 'Content-Type': 'application/json' }
            return {'status':'NOT FOUND'}, 404, { 'Content-Type': 'application/json' }

api.add_resource(collectionresources,'/users/collections','/users/collections/<id>')
api.add_resource(collPublicresources,'/public/collections','/public/collections/<id>')
