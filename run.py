from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(50))
	description = db.Column(db.Text)

class ProductSchema(ma.Schema):
	class Meta:
		fields = ('id','name','description')



product_schema = ProductSchema()

products_schema = ProductSchema(many=True)

class ProductResource(Resource):
	def get(self):
		pro = Product.query.all()
		return products_schema.dump(pro)

	def post(self):
		data=request.json
		pro = Product(name = data['name'], description= data['description'])
		db.session.add(pro)
		db.session.commit()
		return product_schema.dump(pro)

class ProductsResource(Resource):
	def get(self,pk_id):
		pro = Product.query.get_or_404(pk_id)
		return product_schema.dump(pro)

	def patch(self,pk_id):
		pro = Product.query.get_or_404(pk_id)
		data = request.json
		if 'name' in data:
			pro.name=data['name']
		if 'description' in data:
			pro.description=data['description']
		db.session.commit()
		return product_schema.dump(pro)

	def delete(self,pk_id):
		pro  =Product.query.get_or_404(pk_id)
		db.session.delete(pro)
		db.session.commit()
		return '', 204

api.add_resource(ProductResource,'/products')
api.add_resource(ProductsResource,'/product/<int:pk_id>')

if __name__=='__main__':
	app.run(debug=True)