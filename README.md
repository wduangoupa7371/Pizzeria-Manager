# StrongMind Pizza Manager A Full Stack Web Application for Managing Pizzas and Toppings

## Description

This project is a take-home assessment for the Full Stack Engineer position at StrongMind. It demonstrates backend, database integration, deployment, and testing while fulfilling all project requirements.

**Owner credential:**
- username: owner
- password: owner123

**Chef credential:**
- username: chef
- password: chef123

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

  ## Tech Choices and Thought Process

### **Flask**:
I chose Flask for its simplicity, flexibility, and minimal setup requirements, making it ideal for building small to medium-sized web applications. Flask is lightweight, which allows us to keep the application modular and easy to extend in the future. However, if the application were to scale up to handle a significantly larger user base in the future, Django would have been a better choice due to its built-in features for scalability, user authentication, and admin interfaces.


### **Flask-SQLAlchemy**:
For database integration, Flask-SQLAlchemy was selected as the ORM (Object Relational Mapper) because of its tight integration with Flask, ease of use, and support for both SQLite (for local development) and PostgreSQL (for production). 

### **SQLite/PostgreSQL**:
SQLite was used for local development due to its lightweight, file-based nature, making it easy to set up and use without needing a separate database server. For production, PostgreSQL was chosen for its robustness, scalability, and reliability. 

### **Deployment on Render**:
The backend is deployed on Render, a cloud platform that provides a seamless and easy way to deploy Flask applications. Render simplifies deployment by offering free hosting for small applications, automatic scaling, and built-in support for databases like PostgreSQL. It’s an ideal choice for small to medium-sized projects like this one, as it reduces the complexity of deployment and infrastructure management.

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
    pytest test.py --disable-warnings -v
    ```

## Deployment (Live Version)
- Backend deployed on Render → https://pizzeria-manager.onrender.com

