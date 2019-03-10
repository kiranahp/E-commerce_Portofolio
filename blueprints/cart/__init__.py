import random, logging
from blueprints import db
from flask_restful import fields

class carts(db.Model):
	__tablename__ = "cart"
	id = db.Column(db.Integer, primary_key = True)
	product_id = db.Column(db.Integer)
	user_id = db.Column(db.Integer)
	products = db.Column(db.String(1000))
	tot_harga = db.Column(db.String(200))
	users = db.Column(db.String(200))

	response_fields = {
		'id':fields.Integer,
		'product_id':fields.Integer,
		'user_id':fields.Integer,
		'products':fields.String,
		'tot_harga':fields.String,
		'users':fields.String,
	}

	def __init__(self, id, product_id, user_id, products, tot_harga, 
    users):
		self.id = id
		self.product_id = product_id
		self.user_id = user_id
		self.products = products
		self.tot_harga = tot_harga
		self.users = users
	
	def __repr__(self):
		return '<cart %r>' % self.id


