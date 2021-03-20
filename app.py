#Step 2 Climate App

# Import Flask
from flask import Flask, jsonify

#Create an app
app = Flask(__name__)

#Define route
#Home page
@app.route("/")
def home():
    return "Home page"
#List all routes available

#Convert the query results to a dictionary using date as the key and prcp as the value.


#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def prcp_scores():
    return jsonify(prcp_scores)

#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def station_count():
    return jsonify(station_count)

#Query the dates and temperature observations of the most active station for the last year of data
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def year_tobs():
    return jsonify(year_tobs)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def active_station():
    return jsonify(active_station)

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
#@app.route("/api/v1.0/<start>/<end>")
#def station():
    #return jsonify(station)

if __name__ =="__main__":
    app.run(debug=True)
    
