import requests
import xmltodict
from flask import Flask, request
import json

app = Flask(__name__)

BASE_URL = 'https://nourish.me/api/v1/'


def get_menu():
    r = requests.get(BASE_URL+'menu')
    if r.status_code == 200:
        return r.json()
    else:
        return {'status': 'error'}


def get_dish_id(dish_name):
    menu = json.loads(get_menu())
    for dish in menu['dishes']:
        return dish['id'] if dish['name'] == dish_name.strip() else -1


def post_order(orders):
    r = requests.get(BASE_URL + 'bulk/order', data=json.dumps(orders))
    if r.status_code == 200:
        return json.dumps({"status": "success", "description": "order placed successfully!"})
    else:
        return json.dumps({"status": "error", "description": "something went wrong!"})


@app.route("/orders/", methods=['POST'])
def create_order():
    # Parse xml given by Human resource and prepare order
    f = request.files['file']
    with open(f.filename) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    prepare_order = {"orders": []}
    for data in data_dict["employees"]:
        temp_details = {"customer": {"name": data["employee"]["name"], "address": data["employee"]["address"]}} # add customer name and address
        order_data = data["employee"]["order"].split(',')
        temp_details["items"] = [] # Adding multiple order items
        for order in order_data:
            food_details = order.split('x')
            temp_food_details = {"amount": food_details[0], "id": get_dish_id(food_details[1])}
            temp_details["items"].append(temp_food_details)
        prepare_order["orders"].append(temp_details)
    return post_order(prepare_order)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
