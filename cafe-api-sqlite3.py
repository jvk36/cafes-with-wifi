from flask import Flask, jsonify, request, abort
import sqlite3

# FLASK APPLICATION THAT PUBLISHES A REST API TO THE SQLITE TABLE instance/cafes.db:
#
# NOTE: This uses sqlite3 library which is sqlite specific. See 
#  cafe-api-sqlalchemy.py for a general purpose implementation
#  that uses flask_sqlalchemy library instaed.
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
# 1. Database Connection: The connect_db() function establishes a connection 
#  to the SQLite database, and query_db() helps retrieve data from the database.
# 2. GET /cafes: Retrieves all rows from the cafe table. We then convert the rows to 
#  dictionaries using dict(row) and return them as a JSON response.
# 3. GET /cafe/<name>: Retrieves a specific row from the cafe table based on 
#  the cafe’s name. If the cafe is not found, the API returns a 404 error.
# 4. POST /add_cafe: Adds a new cafe to the cafe table. It requires all the fields
#  in the table as in the CREATE TABLE above. If the cafe name already exists, a 
#  400 error is returned.


app = Flask(__name__)

DATABASE = 'instance/cafes.db'

# Helper function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

# Helper function to query the database
def query_db(query, args=(), one=False):
    conn = connect_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# GET /cafes - Retrieve all rows
@app.route('/cafes', methods=['GET'])
def get_cafes():
    cafes = query_db('SELECT * FROM cafe')
    # Convert rows to a list of dictionaries
    cafes_list = [dict(row) for row in cafes]
    return jsonify(cafes_list)

# GET /cafe/<name> - Retrieve individual row by name
@app.route('/cafe/<name>', methods=['GET'])
def get_cafe_by_name(name):
    cafe = query_db('SELECT * FROM cafe WHERE name = ?', [name], one=True)
    if cafe is None:
        abort(404, description="Cafe not found")
    return jsonify(dict(cafe))

# POST /add_cafe - Add a new cafe
@app.route('/add_cafe', methods=['POST'])
def add_cafe():
    new_cafe = request.json

    # Check if the required fields are provided
    if not all(key in new_cafe for key in ("name", "map_url", "img_url", "location", "has_sockets", "has_toilet", "has_wifi", "can_take_calls")):
        abort(400, description="Missing required fields")

    try:
        conn = connect_db()
        conn.execute(
            '''INSERT INTO cafe (name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (new_cafe['name'], new_cafe['map_url'], new_cafe['img_url'], new_cafe['location'],
             new_cafe['has_sockets'], new_cafe['has_toilet'], new_cafe['has_wifi'], new_cafe['can_take_calls'],
             new_cafe.get('seats'), new_cafe.get('coffee_price'))
        )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        abort(400, description="Cafe with this name already exists")
    
    return jsonify({"message": "Cafe added successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
