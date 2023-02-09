import json


def load_data(name):
    with open(name, 'r', encoding='utf-8') as f:
        offers = json.load(f)
        return offers


def add_data_users(name_of_class):
    all_users = load_data('data/users.json')
    users = []
    for i in all_users:
        user_ = name_of_class(
            first_name=i['first_name'],
            last_name=i['last_name'],
            age=i['age'],
            email=i['email'],
            role=i['role'],
            phone=i['phone']
        )
        users.append(user_)
    return users


def add_data_orders(name_of_class):
    all_orders = load_data('data/orders.json')
    orders = []
    for i in all_orders:
        order_ = name_of_class(
            name=i['name'],
            description=i['description'],
            start_date=i['start_date'],
            end_date=i['end_date'],
            address=i['address'],
            price=i['price'],
            customer_id=i['customer_id'],
            executor_id=i['executor_id']
        )
        orders.append(order_)
    return orders


def add_data_offers(name_of_class):
    all_offers = load_data('data/offers.json')
    offers = []
    for i in all_offers:
        offer_ = name_of_class(
            id=i['id'],
            order_id=i['order_id'],
            executor_id=i['executor_id']
        )
        offers.append(offer_)
    return offers
