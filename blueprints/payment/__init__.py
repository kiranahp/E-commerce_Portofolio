import random, logging
from blueprints import db
from flask_restful import fields

class payments(db.Model):
	__tablename__ = "payment"
	id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
	email = db.Column(db.String(200))
	order_refference = db.Column(db.Integer)
	atas_nama = db.Column(db.String(200))
	jumlah_transfer = db.Column(db.String(200))
	date_time = db.Column(db.String(200))
	bukti_transfer = db.Column(db.String(200))
	status = db.Column(db.String(10), default='noCheck')

	response_fields = {
		'id':fields.Integer,
		'email':fields.String,
		'order_refference':fields.Integer,
		'atas_nama':fields.String,
		'jumlah_transfer': fields.String,
        'date_time': fields.String,
        'bukti_transfer': fields.String,
        'status': fields.String
	}

	def __init__(self, id, email, order_refference, atas_nama, jumlah_transfer, 
    date_time, bukti_transfer, status):
		self.id = id
		self.email = email
		self.order_refference = order_refference
		self.atas_nama = atas_nama
		self.jumlah_transfer = jumlah_transfer
		self.date_time = date_time
		self.bukti_transfer = bukti_transfer
		self.status = status
	
	def __repr__(self):
		return '<payment %r>' % self.id


