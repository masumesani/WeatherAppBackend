from flask import Flask, jsonify, request
from flasgger import Swagger
import datetime
import json
import logging
from meteostat import Point, Daily
from datetime import datetime, timedelta 

app = Flask(__name__)
swagger = Swagger(app)

cities = {
    "Tehran":{"lat":35.6892, "lon":51.3890},
    "Paris":{"lat":48.8575, "lon":2.3514},
    "London":{"lat":51.5074, "lon":-0.1278},
    "New York":{"lat":40.7128, "lon":-74.0060},
    "MADRID":{"lat":40.4168, "lon":-3.7038},
    "Copenhagen":{"lat":55.6761, "lon":12.5683},
    "Berlin":{"lat":52.5200, "lon":13.4050},
    "Rome":{"lat":41.9028, "lon":12.4964},
    "Athens":{"lat":37.9838, "lon":23.7275},
    "Istanbul":{"lat":41.0082, "lon":28.9784},
    "Moscow":{"lat":55.7558, "lon":37.6176},
    "Dehli":{"lat":28.7041, "lon":77.1025}, 
    "isfahan":{"lat":32.6546, "lon":51.6679},
}

# Route to get all cities
@app.route('/api/city', methods=['GET'])
def get_cities():
    """
    Get all cities
    ---
    responses:
      200:
        description: A list of books
    """
    
    return jsonify({"cities":list(cities.keys())})

@app.route('/api/weather', methods=['GET'])
def get_weather():

    """
    Get weather of a city
    ---
    parameters:
      - name: city
        in: query
        type: string
        required: true
        description: Filter cities by name
      - name: date 
        in: query
        type: string
        required: false
        description: Date in the format of YYYY-MM-DD
    responses:
      200:
        description: 
    """
    city = request.args.get('city')
    date = request.args.get('date')
    result = cities.get(city)
    if not result or len(result) == 0:
        return jsonify({"error":"City not found"}), 404
           
    lat = result["lat"]
    lon = result["lon"]
    
    now = datetime.now()
    if not date:
        date =  datetime(now.year, now.month, now.day) #datetime.now()
    else:
        got_date = datetime.strptime(date, "%Y-%m-%d")
        date =  datetime(got_date.year, got_date.month, got_date.day)

    # Create Point for Vancouver, BC
    location = Point(lat,lon)

    # Get daily data for 2018
    data = Daily(location, date, date)
    data = data.fetch()
    print(data)
    if(data.empty):
        return jsonify({"error":"Data not found"}), 404
    return jsonify({"temperature":data.iloc[0]["tavg"]})
     



if __name__ == '__main__':
    app.run(debug=True)
