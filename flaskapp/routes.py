from flask import Blueprint, request, jsonify
from db_setup import db, Topping, Pizza, pizza_toppings
from sqlalchemy import func


routes = Blueprint("routes", __name__)

@routes.route("/toppings", methods=["GET"])
def get_toppings():
    toppings = Topping.query.all()
    return jsonify([{"id": t.id, "name": t.name} for t in toppings])

@routes.route("/toppings/<int:id>", methods=["GET"])
def get_topping(id):
    topping = Topping.query.get(id)
    if not topping:
        return jsonify({"message": "Topping not found"}), 404
    return jsonify({"id": topping.id, "name": topping.name})

@routes.route("/toppings", methods=["POST"])
def add_topping():
    data = request.json
    if Topping.query.filter(func.lower(Topping.name) == func.lower(data["name"])).first():
        return jsonify({"message": "Topping already exists"}), 400
    new_topping = Topping(name=data["name"])
    db.session.add(new_topping)
    db.session.commit()
    return jsonify({"id": new_topping.id, "name": new_topping.name}), 201

@routes.route("/toppings/<int:id>", methods=["DELETE"])
def delete_topping(id):
    topping = Topping.query.get(id)
    if not topping:
        return jsonify({"message": "Topping not found"}), 404
    db.session.delete(topping)
    db.session.commit()
    return jsonify({"message": "Topping deleted"}), 200

@routes.route("/toppings/<int:id>", methods=["PUT"])
def update_topping(id):
    topping = Topping.query.get(id)
    if not topping:
        return jsonify({"message": "Topping not found"}), 404
    data = request.json
    if data.get("name") and data["name"] != topping.name:
        if data.get("name") and data["name"] != topping.name:
            if Topping.query.filter(func.lower(Topping.name) == func.lower(data["name"])).first():
                return jsonify({"message": "Topping name already exists"}), 400
        topping.name = data["name"]
    db.session.commit()
    return jsonify({"id": topping.id, "name": topping.name})

@routes.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{"id": p.id, "name": p.name, "toppings": [t.name for t in p.toppings]} for p in pizzas])

@routes.route("/pizzas", methods=["POST"])
def add_pizza():
    data = request.json
    if Pizza.query.filter(func.lower(Pizza.name) == func.lower(data["name"])).first():
        return jsonify({"message": "Pizza already exists"}), 400
    new_pizza = Pizza(name=data["name"])
    for topping_name in data.get("toppings", []):
        topping = Topping.query.filter_by(name=topping_name).first()
        if topping:
            new_pizza.toppings.append(topping)
    db.session.add(new_pizza)
    db.session.commit()
    return jsonify({"id": new_pizza.id, "name": new_pizza.name, "toppings": [t.name for t in new_pizza.toppings]}), 201

@routes.route("/pizzas/<int:id>", methods=["DELETE"])
def delete_pizza(id):
    pizza = Pizza.query.get(id)
    if not pizza:
        return jsonify({"message": "Pizza not found"}), 404
    db.session.delete(pizza)
    db.session.commit()
    return jsonify({"message": "Pizza deleted"}), 200

@routes.route("/pizzas/<int:id>", methods=["GET"])
def get_pizza(id):
    pizza = Pizza.query.get(id)
    if not pizza:
        return jsonify({"message": "Pizza not found"}), 404
    return jsonify({"id": pizza.id, "name": pizza.name, "toppings": [t.name for t in pizza.toppings]})

@routes.route("/pizzas/<int:id>", methods=["PUT"])
def update_pizza(id):
    pizza = Pizza.query.get(id)
    if not pizza:
        return jsonify({"message": "Pizza not found"}), 404

    data = request.json

    if data.get("name") and data["name"] != pizza.name:
        if Pizza.query.filter(func.lower(Pizza.name) == func.lower(data["name"])).first():
            return jsonify({"message": "Pizza name already exists"}), 400
        pizza.name = data["name"]

    if "toppings" in data:
        topping_names = data["toppings"]
        toppings = Topping.query.filter(Topping.name.in_(topping_names)).all()

        if len(toppings) != len(topping_names):
            missing_toppings = set(topping_names) - set(t.name for t in toppings)
            return jsonify({"message": f"Toppings not found: {', '.join(missing_toppings)}"}), 400

        pizza.toppings = toppings

    db.session.commit()
    return jsonify({
        "id": pizza.id,
        "name": pizza.name,
        "toppings": [t.name for t in pizza.toppings]
    })

@routes.route("/pizzas/<int:id>/toppings", methods=["PUT"])
def update_pizza_toppings(id):
    pizza = Pizza.query.get(id)
    if not pizza:
        return jsonify({"message": "Pizza not found"}), 404
    data = request.json
    topping_names = data.get("toppings", [])
    pizza.toppings = []
    for topping_name in topping_names:
        topping = Topping.query.filter_by(name=topping_name).first()
        if topping:
            pizza.toppings.append(topping)
    db.session.commit()
    return jsonify({"id": pizza.id, "name": pizza.name, "toppings": [t.name for t in pizza.toppings]})