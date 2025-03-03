from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from db_setup import db  # Import db from db_setup
from routes import routes  # Import the routes Blueprint

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.secret_key = '02882737173'

app.register_blueprint(routes)

@app.route("/")
def index():
    return render_template("index.html")

USERS = {
    "owner": "owner123",
    "chef": "chef123"
}



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        role = data.get('role', '').lower().strip()
        password = data.get('password', '').strip()

        if role in USERS and USERS[role] == password:
            session['role'] = role
            return jsonify({"success": True, "redirect": url_for(f"{role}_dashboard")})
        else:
            return jsonify({"success": False}), 401

    return render_template("index.html")

@app.route('/owner_dashboard')
def owner_dashboard():
    if session.get('role') != 'owner':
        return redirect(url_for('login'))
    return render_template('owner_dashboard.html')

@app.route('/chef_dashboard')
def chef_dashboard():
    if session.get('role') != 'chef':
        return redirect(url_for('login'))
    return render_template('chef_dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)