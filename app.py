from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from utils import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:?charset=utf-8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def instance_to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship("User")
    executor = db.relationship("Order")

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])

    def instance_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


with app.app_context():
    db.create_all()

    users = add_data_users(User)

    db.session.add_all(users)
    db.session.commit()

    orders = add_data_orders(Order)

    db.session.add_all(orders)
    db.session.commit()

    offers = add_data_offers(Offer)

    db.session.add_all(offers)
    db.session.commit()


@app.route("/users", methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        result = []
        all_users = User.query.all()
        for user in all_users:
            result.append(user.instance_to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age=data.get('age'),
            email=data.get('email'),
            role=data.get('role'),
            phone=data.get('phone')
        )
        db.session.add(user)
        db.session.commit()
        return 'Данные записаны)'


@app.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
def get_user_with_id(uid):
    if request.method == 'GET':
        user = User.query.get(uid)
        return jsonify(user.instance_to_dict())
    elif request.method == 'PUT':
        data_to_update = json.loads(request.data)
        user = User.query.get(uid)

        user.id = data_to_update['id']
        user.first_name = data_to_update["first_name"]
        user.last_name = data_to_update["last_name"]
        user.age = data_to_update['age']
        user.email = data_to_update['email']
        user.role = data_to_update['role']
        user.phone = data_to_update['phone']

        db.session.add(user)
        db.session.commit()
        return "Данные обновлены)"
    elif request.method == 'DELETE':
        user_to_delete = User.query.get(uid)
        db.session.delete(user_to_delete)
        db.session.commit()
        return 'Данные удалены)'


@app.route("/orders", methods=['GET', 'POST'])
def get_orders():
    if request.method == 'GET':
        result = []
        all_orders = Order.query.all()
        for order in all_orders:
            result.append(order.instance_to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        order = Order(
            name=data.get('name'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            address=data.get('address'),
            price=data.get('price'),
            customer_id=data.get('customer_id'),
            executor_id=data.get('executor_id')
        )
        db.session.add(order)
        db.session.commit()
        return 'Данные записаны)'


@app.route('/orders/<uid>', methods=['GET', 'PUT', 'DELETE'])
def get_orders_with_id(uid):
    if request.method == 'GET':
        order = Order.query.get(uid)
        return jsonify(order.instance_to_dict())
    elif request.method == 'PUT':
        data_to_update = json.loads(request.data)
        order = Order.query.get(uid)

        order.id = data_to_update['id']
        order.name = data_to_update["name"]
        order.description = data_to_update["description"]
        order.start_date = data_to_update['start_date']
        order.end_date = data_to_update['end_date']
        order.price = data_to_update['price']
        order.customer_id = data_to_update['customer_id']
        order.executor_id = data_to_update['executor_id']

        db.session.add(order)
        db.session.commit()
        return "Данные обновлены)"
    elif request.method == 'DELETE':
        order_to_delete = Order.query.get(uid)
        db.session.delete(order_to_delete)
        db.session.commit()
        return 'Данные удалены)'


@app.route("/offers", methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        result = []
        all_offers = Offer.query.all()
        for offer in all_offers:
            result.append(offer.to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        offer = Offer(
            id=data.get('id'),
            order_id=data.get('order_id'),
            executor_id=data.get('executor_id')
        )
        db.session.add(offer)
        db.session.commit()
        return 'Данные записаны)'


@app.route('/offers/<uid>', methods=['GET', 'PUT', 'DELETE'])
def get_offer_with_id(uid):
    if request.method == 'GET':
        offer = Offer.query.get(uid)
        return jsonify(offer.instance_to_dict())
    elif request.method == 'PUT':
        data_to_update = json.loads(request.data)
        offer = Offer.query.get(uid)

        offer.id = data_to_update['id']
        offer.name = data_to_update["name"]
        offer.description = data_to_update["description"]
        offer.start_date = data_to_update['start_date']
        offer.end_date = data_to_update['end_date']
        offer.price = data_to_update['price']
        offer.customer_id = data_to_update['customer_id']
        offer.executor_id = data_to_update['executor_id']

        db.session.add(offer)
        db.session.commit()
        return "Данные обновлены)"
    elif request.method == 'DELETE':
        offer_to_delete = Offer.query.get(uid)
        db.session.delete(offer_to_delete)
        db.session.commit()
        return 'Данные удалены)'


if __name__ == "__main__":
    app.run()
