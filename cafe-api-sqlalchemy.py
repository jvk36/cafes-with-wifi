from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

# FLASK APPLICATION THAT PUBLISHES A REST API TO THE SQLITE TABLE instance/cafes.db:
#
# NOTE: This uses flask_sqlalchemy library which is general purpose instead of 
#  the sqlite only sqlite3 library. For example, to switch to a PostgreSQL 
#  relational DB instance, replace 
#   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
#  with
#   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
#
# API DETAILS:
#
# 1. GET /cafes: Retrieve all rows from the cafe table.
# 2. GET /cafe/<name>: Retrieve a specific row by the cafe’s name.
# 3. POST /add_cafe: Add a new cafe to the cafe table.
#
# DATABASE DDL:
#
# CREATE TABLE cafe (
#     id INTEGER PRIMARY KEY,
#     name VARCHAR(250) NOT NULL UNIQUE,
#     map_url VARCHAR(500) NOT NULL,
#     img_url VARCHAR(500) NOT NULL,
#     location VARCHAR(250) NOT NULL,
#     has_sockets BOOLEAN NOT NULL,
#     has_toilet BOOLEAN NOT NULL,
#     has_wifi BOOLEAN NOT NULL,
#     can_take_calls BOOLEAN NOT NULL,
#     seats VARCHAR(250),
#     coffee_price VARCHAR(250)
# );
#
# EXPLANATION OF HOW IT WORKS?
#
# 1. DATABASE CONFIGURATION: The SQLite database is configured using 
#    SQLALCHEMY_DATABASE_URI, which points to sqlite:///cafes.db. You can easily 
#    switch to another database by changing the URI (e.g., PostgreSQL or MySQL).
# 2. Cafe MODEL: The Cafe model represents the structure of the cafe table. 
#    SQLAlchemy automatically maps this model to the cafe table.
# 3. ROUTES:
#   a) GET /cafes: Retrieves all cafes from the database, converts the results 
#      to a list of dictionaries, and returns them as a JSON response.
#   b) GET /cafe/<name>: Retrieves a cafe by its name using SQLAlchemy’s query 
#      interface. If the cafe is not found, a 404 error is returned.
#   c) POST /add_cafe: Adds a new cafe to the cafe table. It first checks if all 
#      required fields are present in the request, creates a new Cafe instance, 
#      and commits it to the database. If the cafe name is already present, the 
#      app will handle the error and return a 400 error response.
# 4. ERROR HANDLING: The app uses abort() to handle errors such as missing 
#    required fields, duplicate cafe names, or database errors.
# 5. DATABASE CREATION: @app.before_first_request: Creates the tables in the 
#    database before handling the first request.
#    NOTE: The database creation code is commented out as we assume it was 
#          created previously and is available under instance/cafe.db
#  

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
# To use a PostgreSQL relational DB instance, replace above line with below:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Cafe model
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))

# Create the database and tables (only needs to be run once)
# @app.before_first_request
# def create_tables():
#     db.create_all()

# GET /cafes - Retrieve all rows
@app.route('/cafes', methods=['GET'])
def get_cafes():
    cafes = Cafe.query.all()
    # Convert the cafes to a list of dictionaries
    cafes_list = [{
        'id': cafe.id,
        'name': cafe.name,
        'map_url': cafe.map_url,
        'img_url': cafe.img_url,
        'location': cafe.location,
        'has_sockets': cafe.has_sockets,
        'has_toilet': cafe.has_toilet,
        'has_wifi': cafe.has_wifi,
        'can_take_calls': cafe.can_take_calls,
        'seats': cafe.seats,
        'coffee_price': cafe.coffee_price
    } for cafe in cafes]
    return jsonify(cafes_list)

# GET /cafe/<name> - Retrieve individual row by name
@app.route('/cafe/<name>', methods=['GET'])
def get_cafe_by_name(name):
    cafe = Cafe.query.filter_by(name=name).first()
    if cafe is None:
        abort(404, description="Cafe not found")
    return jsonify({
        'id': cafe.id,
        'name': cafe.name,
        'map_url': cafe.map_url,
        'img_url': cafe.img_url,
        'location': cafe.location,
        'has_sockets': cafe.has_sockets,
        'has_toilet': cafe.has_toilet,
        'has_wifi': cafe.has_wifi,
        'can_take_calls': cafe.can_take_calls,
        'seats': cafe.seats,
        'coffee_price': cafe.coffee_price
    })

# POST /add_cafe - Add a new cafe
@app.route('/add_cafe', methods=['POST'])
def add_cafe():
    new_cafe_data = request.json

    if not all(key in new_cafe_data for key in ("name", "map_url", "img_url", "location", "has_sockets", "has_toilet", "has_wifi", "can_take_calls")):
        abort(400, description="Missing required fields")

    # Create a new Cafe instance
    new_cafe = Cafe(
        name=new_cafe_data['name'],
        map_url=new_cafe_data['map_url'],
        img_url=new_cafe_data['img_url'],
        location=new_cafe_data['location'],
        has_sockets=new_cafe_data['has_sockets'],
        has_toilet=new_cafe_data['has_toilet'],
        has_wifi=new_cafe_data['has_wifi'],
        can_take_calls=new_cafe_data['can_take_calls'],
        seats=new_cafe_data.get('seats'),
        coffee_price=new_cafe_data.get('coffee_price')
    )

    try:
        db.session.add(new_cafe)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(400, description=f"Error: {str(e)}")
    
    return jsonify({"message": "Cafe added successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
