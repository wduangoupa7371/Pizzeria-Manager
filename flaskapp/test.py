import pytest
import json
from flaskapp.pizzaManager import app, db


@pytest.fixture
def test_app():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()


class TestToppings:

    def test_get_toppings_empty(self, client):
        response = client.get('/toppings')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_create_topping(self, client):
        response = client.post(
            '/toppings',
            data=json.dumps({'name': 'Pepperoni'}),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Pepperoni'
        assert 'id' in data

    def test_create_duplicate_topping(self, client):
        client.post(
            '/toppings',
            data=json.dumps({'name': 'Mushrooms'}),
            content_type='application/json'
        )

        response = client.post(
            '/toppings',
            data=json.dumps({'name': 'Mushrooms'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already exists' in data.get('message', '')

    def test_get_topping_by_id(self, client):
        resp = client.post(
            '/toppings',
            data=json.dumps({'name': 'Onions'}),
            content_type='application/json'
        )
        topping_id = json.loads(resp.data)['id']

        response = client.get(f'/toppings/{topping_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Onions'
        assert data['id'] == topping_id

    def test_get_nonexistent_topping(self, client):
        response = client.get('/toppings/999')
        assert response.status_code == 404

    def test_update_topping(self, client):
        resp = client.post(
            '/toppings',
            data=json.dumps({'name': 'Bell Pepper'}),
            content_type='application/json'
        )
        topping_id = json.loads(resp.data)['id']

        response = client.put(
            f'/toppings/{topping_id}',
            data=json.dumps({'name': 'Green Pepper'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Green Pepper'
        assert data['id'] == topping_id

    def test_update_topping_duplicate_name(self, client):
        client.post(
            '/toppings',
            data=json.dumps({'name': 'Pineapple'}),
            content_type='application/json'
        )

        resp = client.post(
            '/toppings',
            data=json.dumps({'name': 'Ham'}),
            content_type='application/json'
        )
        topping_id = json.loads(resp.data)['id']

        response = client.put(
            f'/toppings/{topping_id}',
            data=json.dumps({'name': 'Pineapple'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already exists' in data.get('message', '')

    def test_delete_topping(self, client):
        resp = client.post(
            '/toppings',
            data=json.dumps({'name': 'Olives'}),
            content_type='application/json'
        )
        topping_id = json.loads(resp.data)['id']

        response = client.delete(f'/toppings/{topping_id}')
        assert response.status_code == 200

        response = client.get(f'/toppings/{topping_id}')
        assert response.status_code == 404

    def test_delete_nonexistent_topping(self, client):
        response = client.delete('/toppings/999')
        assert response.status_code == 404


class TestPizzas:

    @pytest.fixture
    def sample_toppings(self, client):
        toppings = ['Cheese', 'Pepperoni', 'Mushrooms', 'Sausage']
        topping_ids = []

        for topping in toppings:
            resp = client.post(
                '/toppings',
                data=json.dumps({'name': topping}),
                content_type='application/json'
            )
            topping_ids.append(json.loads(resp.data)['id'])

        return toppings, topping_ids

    def test_get_pizzas_empty(self, client):
        response = client.get('/pizzas')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_create_pizza(self, client, sample_toppings):
        toppings_list, _ = sample_toppings
        response = client.post(
            '/pizzas',
            data=json.dumps({
                'name': 'Meat Lovers',
                'toppings': ['Cheese', 'Pepperoni', 'Sausage']
            }),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Meat Lovers'
        assert 'id' in data

        response = client.get(f'/pizzas/{data["id"]}')
        pizza_data = json.loads(response.data)
        assert set(pizza_data['toppings']) == set(['Cheese', 'Pepperoni', 'Sausage'])

    def test_create_duplicate_pizza(self, client, sample_toppings):
        toppings_list, _ = sample_toppings

        client.post(
            '/pizzas',
            data=json.dumps({
                'name': 'Veggie Supreme',
                'toppings': ['Cheese', 'Mushrooms']
            }),
            content_type='application/json'
        )

        response = client.post(
            '/pizzas',
            data=json.dumps({
                'name': 'Veggie Supreme',
                'toppings': ['Cheese', 'Mushrooms']
            }),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already exists' in data.get('message', '')

    def test_get_pizza_by_id(self, client, sample_toppings):
        toppings_list, _ = sample_toppings

        resp = client.post(
            '/pizzas',
            data=json.dumps({
                'name': 'Hawaiian',
                'toppings': ['Cheese']
            }),
            content_type='application/json'
        )
        pizza_id = json.loads(resp.data)['id']

        response = client.get(f'/pizzas/{pizza_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Hawaiian'
        assert data['id'] == pizza_id
        assert 'Cheese' in data['toppings']

    def test_get_nonexistent_pizza(self, client):
        response = client.get('/pizzas/999')
        assert response.status_code == 404

    def test_update_pizza_name(self, client, sample_toppings):
        toppings_list, _ = sample_toppings

        resp = client.post(
            '/pizzas',
            data=json.dumps({
                'name': 'Margherita',
                'toppings': ['Cheese']
            }),
            content_type='application/json'
        )
        pizza_id = json.loads(resp.data)['id']

        response = client.put(
            f'/pizzas/{pizza_id}',
            data=json.dumps({'name': 'Super Margherita'}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Super Margherita'
        assert data['id'] == pizza_id
        assert 'Cheese' in data['toppings']

    def test_update_pizza_toppings(self, client, sample_toppings):
        toppings_list, _ = sample_toppings

        resp = client.post(
            '/pizzas',
            data=json.dumps({
                'name': 'Supreme',
                'toppings': ['Cheese', 'Pepperoni']
            }),
            content_type='application/json'
        )
        pizza_id = json.loads(resp.data)['id']

        response = client.put(
            f'/pizzas/{pizza_id}/toppings',
            data=json.dumps({
                'toppings': ['Cheese', 'Pepperoni', 'Mushrooms', 'Sausage']
            }),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Supreme'
        assert set(data['toppings']) == set(['Cheese', 'Pepperoni', 'Mushrooms', 'Sausage'])

    def test_update_pizza_duplicate_name(self, client, sample_toppings):
        toppings_list, _ = sample_toppings

        client.post(
            '/pizzas',
            data=json.dumps({
                'name': 'Cheese Pizza',
                'toppings': ['Cheese']
            }),
            content_type='application/json'
        )

        resp = client.post(
            '/pizzas',
            data=json.dumps({
                'name': 'Pepperoni Pizza',
                'toppings': ['Cheese', 'Pepperoni']
            }),
            content_type='application/json'
        )
        pizza_id = json.loads(resp.data)['id']

        response = client.put(
            f'/pizzas/{pizza_id}',
            data=json.dumps({'name': 'Cheese Pizza'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'already exists' in data.get('message', '')

    def test_delete_pizza(self, client, sample_toppings):
        toppings_list, _ = sample_toppings

        resp = client.post(
            '/pizzas',
            data=json.dumps({
                'name': 'BBQ Chicken',
                'toppings': ['Cheese']
            }),
            content_type='application/json'
        )
        pizza_id = json.loads(resp.data)['id']

        response = client.delete(f'/pizzas/{pizza_id}')
        assert response.status_code == 200

        response = client.get(f'/pizzas/{pizza_id}')
        assert response.status_code == 404

    def test_delete_nonexistent_pizza(self, client):
        response = client.delete('/pizzas/999')
        assert response.status_code == 404