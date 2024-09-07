from flask import Flask, render_template, request, redirect, url_for, flash
import requests

# RUNNING THE APP:
#
# 1. Ensure your API is running on port 5000. Run either cafe-api-sqlite3.py
#    or cafe-api-sqlalchemy.py. 
# 2. Run this web app file on port 5001.
# 3. Access the app by navigating to http://127.0.0.1:5001 in your browser.
# 4. You can view the list of cafes and add new ones using the form at
#    http://127.0.0.1:5001/add_cafe .
#
# APPLICATION STRUCTURE:
#
# GET /: Displays the list of cafes retrieved from the API in a Bootstrap 
#        grid layout.
# GET /add_cafe: Displays a form to add a new cafe.
# POST /add_cafe: Sends the form data to the API (via a POST request) to 
#                 add the cafe.
#
# KEY POINTS:
# 
# Interaction with API: The web app (running on port 5001) interacts with 
#   the REST API (running on port 5000) using the requests library.
#
# Aesthetic Layout: The cafes are displayed using Bootstrap's grid system. 
#   Each cafe is shown as a card with an image, cafe name, and key details 
#   like location, seats, coffee price, and features (like Wi-Fi, sockets, 
#   etc.).
# 
# Form for Adding Cafes: The form at /add_cafe collects all necessary 
#   information from the user to create a new cafe, and upon submission, the 
#   data is sent to the API. A success or failure message is displayed using 
#   Flask's flash feature.
#
# Bootstrap: The entire layout is designed with Bootstrap to ensure the web 
#   application is responsive and visually appealing.
#
# Jinja2: Jinja2 templating is used to loop through the list of cafes and 
#   dynamically render each cafe’s data in the index.html page.
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# API base URL
API_URL = 'http://127.0.0.1:5000'

# Route to display all cafes
@app.route('/')
def index():
    # Fetch the cafes from the API
    response = requests.get(f'{API_URL}/cafes')
    if response.status_code == 200:
        cafes = response.json()
    else:
        cafes = []
    return render_template('index.html', cafes=cafes)

# Route to show the form to add a new cafe
@app.route('/add_cafe', methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        # Collect form data
        new_cafe_data = {
            "name": request.form.get('name'),
            "map_url": request.form.get('map_url'),
            "img_url": request.form.get('img_url'),
            "location": request.form.get('location'),
            "has_sockets": request.form.get('has_sockets') == 'yes',
            "has_toilet": request.form.get('has_toilet') == 'yes',
            "has_wifi": request.form.get('has_wifi') == 'yes',
            "can_take_calls": request.form.get('can_take_calls') == 'yes',
            "seats": request.form.get('seats'),
            "coffee_price": request.form.get('coffee_price')
        }

        # Send data to the API
        response = requests.post(f'{API_URL}/add_cafe', json=new_cafe_data)

        if response.status_code == 201:
            flash('Cafe added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Failed to add cafe. Please try again.', 'danger')

    return render_template('add_cafe.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
