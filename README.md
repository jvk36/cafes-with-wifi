# INSTALL PREREQUISITES:

pip install -r requirements.txt

## HOW TO RUN THE APPLICATION?

1. Publish the API by running either cafe-api-sqlite3.py or cafe-api-sqlalchemy.py
   from the terminal. It uses port 5000.
2. Use another terminal to run the web application cafe-webapp.py. It uses port 5001.

## TESTING THE API:

NOTE: cafe-api-sqlite3.py and cafe-api-sqlalchemy.py are functionally synonymous.
So, run either of those Flask programs and you can access the API from port 5000.

### Add a New Cafe (POST /add_cafe):

curl -X POST -H "Content-Type: application/json" -d '{
  "name": "Cafe Blue",
  "map_url": "https://maps.google.com/cafe_blue",
  "img_url": "https://images.com/cafe_blue.jpg",
  "location": "123 Main St",
  "has_sockets": true,
  "has_toilet": true,
  "has_wifi": true,
  "can_take_calls": true,
  "seats": "50",
  "coffee_price": "$5"
}' http://127.0.0.1:5000/add_cafe

Windows Powershell version:

$data = @{
    name         = "Cafe Blue"
    map_url      = "https://maps.google.com/cafe_blue"
    img_url      = "https://images.com/cafe_blue.jpg"
    location     = "123 Main St"
    has_sockets  = $true
    has_toilet   = $true
    has_wifi     = $true
    can_take_calls = $true
    seats        = "50"
    coffee_price = "$5"
}

Convert the hashtable to a JSON string:

$jsonData = $data | ConvertTo-Json

Invoke the REST method to send the POST request:

Invoke-RestMethod -Uri "http://127.0.0.1:5000/add_cafe" -Method Post -Body $jsonData -ContentType "application/json"


### Get All Cafes (GET /cafes):

curl http://127.0.0.1:5000/cafes

### Get a Cafe by Name (GET /cafe/<name>):

curl http://127.0.0.1:5000/cafe/Cafe%20Blue

### NOTE - Explanation of the PowerShell POST usage above:

$data: A PowerShell hashtable representing the JSON data.
ConvertTo-Json: Converts the PowerShell hashtable into a JSON string that can be sent in the body of the request.
Invoke-RestMethod:
-Uri specifies the API endpoint (/add_cafe).
-Method Post specifies the HTTP method.
-Body sends the JSON data as the request body.
-ContentType "application/json" ensures the content type is correctly set to JSON.
