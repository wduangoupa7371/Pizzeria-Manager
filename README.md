# StrongMind Pizza Manager A Full Stack Web Application for Managing Pizzas and Toppings

## Description

This project is a take-home assessment for the Full Stack Engineer position at StrongMind. It demonstrates backend, database integration, deployment, and testing while fulfilling all project requirements.

The app allows: 

- Pizza store owners to manage toppings (CRUD operations).
- Pizza chefs to create, update, and delete pizzas with toppings.
- Data persistence using Flask-SQLAlchemy (SQLite for local testing, PostgreSQL for production).
- Backend deployed on Render.

## 🛠 Project Requirements

### Manage Toppings
As a pizza store owner I should be able to manage toppings available for my pizza chefs.

- It should allow me to see a list of available toppings
- It should allow me to add a new topping
- It should allow me to delete an existing topping
- It should allow me to update an existing topping
- It should not allow me to enter duplicate toppings

### Manage Pizzas
As a pizza chef I should be able to create new pizza master pieces.

- It should allow me to see a list of existing pizzas and their toppings
- It should allow me to create a new pizza and add toppings to it
- It should allow me to delete an existing pizza
- It should allow me to update an existing pizza
- It should allow me to update toppings on an existing pizza
- It should not allow me to enter duplicate pizzas

## Tech Stack

- **Backend**: Flask (Python), Flask-SQLAlchemy, Flask-RESTful
- **Database**: SQLite (local) / PostgreSQL (Render production)
- **Testing**: pytest (11 test cases)
- **Deployment**: Backend on Render

## Prerequisites

Before running the project, ensure you have:

- Python 3.8+ installed
- Flask & dependencies installed

## ** Installation & Setup**

1. Clone the Repository
    ```bash
    git clone https://github.com/yourusername/strongmind_pizza.git
    cd strongmind
    ```

2. Running the Application Locally
    ```bash
    cd pizzeria-manager
    python -m venv venv
    venv/bin/activate
    pip install -r requirements.txt

    cd flaskapp
    python pizzaManager.py
    ```

3. To run the tests after installing requirements and activating virtual environment:
    ```bash
    cd flaskapp
    pytest test.py
    ```

## Deployment (Live Version)
- Backend deployed on Render → https://pizzeria-manager.onrender.com

