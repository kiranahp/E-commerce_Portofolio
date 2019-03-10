import random, logging
from blueprints import db
from flask_restful import fields
# from blueprints.client import Clients

class Users(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
	email = db.Column(db.String(200))
	password = db.Column(db.String(200))
	name = db.Column(db.String(200))
	phone_number = db.Column(db.String(200))
	status_admin = db.Column(db.String(5), default="user")

	response_fields = {
		'id':fields.Integer,
		'email':fields.String,
		'password':fields.String,
		'name':fields.String,
		'phone_number':fields.Integer,
		'status_admin': fields.String
	}

	def __init__(self, id, email, password, name, phone_number, status_admin):
		self.id = id
		self.email = email
		self.password = password
		self.name = name 
		self.phone_number = phone_number
		self.status_admin = status_admin
	
	def __repr__(self):
		return '<User %r>' % self.id


