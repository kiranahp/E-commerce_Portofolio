import random, logging
from blueprints import db
from flask_restful import fields

class Collections(db.Model):
	__tablename__ = "collection"
	id = db.Column(db.Integer, primary_key = True, autoincrement = True, unique = True)
	kode_barang = db.Column(db.String(200))
	harga = db.Column(db.String(200))
	deskripsi = db.Column(db.String(200))
	label = db.Column(db.String(200), default='new')
	kategori = db.Column(db.String(200))


	response_fields = {
		'id':fields.Integer,
		'kode_barang':fields.String,
		'harga':fields.String,
		'deskripsi':fields.String,
		'label':fields.String,
		'kategori':fields.String,
	}

	def __init__(self, id, kode_barang, harga, deskripsi, label, kategori):
		self.id = id
		self.kode_barang = kode_barang
		self.harga = harga
		self.deskripsi = deskripsi
		self.label = label
		self.kategori = kategori 
	
	def __repr__(self):
		return '<collection %r>' % self.id


