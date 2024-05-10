from flask import Flask, jsonify, request
from flasgger import Swagger
import datetime
import json
import logging
from meteostat import Point, Daily, Hourly
from datetime import datetime, timedelta 

app = Flask(__name__)
swagger = Swagger(app)

cities = {
    "Tehran":{"lat":35.6892, "long":51.3890},
    "Paris":{"lat":48.8575, "long":2.3514},
    "London":{"lat":51.5074, "long":-0.1278},
    "New York":{"lat":40.7128, "long":-74.0060},
    "Madrid":{"lat":40.4168, "long":-3.7038},
    "Copenhagen":{"lat":55.6761, "long":12.5683},
    "Berlin":{"lat":52.5200, "long":13.4050},
    "Rome":{"lat":41.9028, "long":12.4964},
    "Athens":{"lat":37.9838, "long":23.7275},
    "Istanbul":{"lat":41.0082, "long":28.9784},
    "Moscow":{"lat":55.7558, "long":37.6176},
    "Dehli":{"lat":28.7041, "long":77.1025}, 
    "isfahan":{"lat":32.6546, "long":51.6679},
}

# Route to get all cities
@app.route('/api/city', methods=['GET'])
def get_cities():
    """
    Get all cities
    ---
    responses:
      200:
        description: A list of cities
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
      - name: country
        in: query
        type: string
        required: true
        description: Filter countries by name
      - name: startDate 
        in: query
        type: string
        required: false
        description: Date in the format of YYYY-MM-DD
      - name: endDate 
        in: query
        type: string
        required: false
        description: Date in the format of YYYY-MM-DD
    responses:
      200:
        description: 
    """
    city = request.args.get('city')
    country = request.args.get('country')
    if not city:
        return jsonify({"error":"City cannot be null"}), 400
        
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')

    if endDate and not startDate:
        return jsonify({"error":"Cannot parse end date without start date"}), 400
        
    result = cities.get(city)
    if not result or len(result) == 0:
        return jsonify({"error":"City not found"}), 404
           
    lat = result["lat"]
    long = result["long"]
    
    now = datetime.now()
    if not startDate:
        startDate =  datetime(now.year-1, now.month, now.day) 
        endDate= datetime(now.year-1, now.month, now.day+1)

    elif not endDate:
      
        got_start_date = datetime.strptime(startDate, "%Y-%m-%d")
        startDate =  datetime(got_start_date.year-1, got_start_date.month, got_start_date.day)
        endDate = datetime(startDate.year, startDate.month, startDate.day+1)
    else:
        got_start_date = datetime.strptime(startDate, "%Y-%m-%d")
        startDate = datetime(got_start_date.year-1, got_start_date.month, got_start_date.day)
        got_end_date = datetime.strptime(endDate, "%Y-%m-%d")
        endDate =  datetime(got_end_date.year-1, got_end_date.month, got_end_date.day)
    # Create Point for wanted city
    location = Point(lat,long)

    # Get daily data for last year same date
    data = Daily(location, startDate,endDate)
    data = data.fetch()
    
    print(data)
    if(data.empty):
        return jsonify({"error":"Data not found"}), 404
    weather_data = [{
                      "date":str(i),
                      "tavg":d["tavg"],
                      "tavgUnit":"°C",
                      "tavgDisplayname":"Average Temperature",
                      "tmax":d["tmax"],
                      "tmaxUnit":"°C",
                      "tmaxDisplayname":"Max Temperature",
                      "tmin":d["tmin"],
                      "tminUnit":"°C",
                      "tminDisplayname":"Min Temperature",
                      "prcp":d["prcp"],
                      "prcpUnit":"mm",
                      "prcpDisplayname":"Precipitation",
                      "wspd":d["wspd"],
                      "wspdUnit":"km/h",
                      "wspdDisplayname":"Wind Speed"
                    } for (i,d) in data.iterrows()]
    return jsonify (
        {
          "country":country,
          "city":city,
          "lat":lat,
          "long":long,
          "startDate": startDate,
          "dataLength": data.size,
          "weatherData":weather_data
        })
     



if __name__ == '__main__':
    app.run(debug=True)
