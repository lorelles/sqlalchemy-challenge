### Step 2 Climate App ###

# Import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask
from flask import Flask, jsonify

#### Database Setup ###
engine = create_engine("sqlite:///../hawaii.sqlite")
# Reflect existing database into new model
Base = automap_base()
# Reflect tables
Base.prepare(engine, reflect=True)
# Save reference to tables
station = Base.classes.station
measurement = Base.classes.measurement
# Create session
session = Session(engine)

# Create an app
app = Flask(__name__)

### Define routes ###

# Home page
# List all routes available
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"JSON representation of precipitation scores:<br/>"       
        f"<a href='/api/v1.0/precipitation'></a><br/>"      
        f"JSON list of stations from the dataset:<br/>"
        f"<a href='/api/v1.0/stations'></a><br/>"
        f"JSON list of temperature observations (TOBS) for previous year:<br/>"
        f"<a href='/api/v1.0/tobs'></a><br/>"
        f"Return JSON list of minimum, average, and max temperature for given start or start-end range:<br/>"
        f"<a href='/api/v1.0/<start>/<end>'></a><br/>"
        f"Calculate TMIN, TAVG, and TMAX for all dates greater or equal to start date:<br/>"
        f"<a'/api/v1.0/<start>></a><br/>"
        f"Calculate TMIN, TAVG, and TMAX for dates between start and end dates:<br/>"
        f"<a hreaf='/api/v1.0/<start>'></a><br/>"
    )



#Convert the query results to a dictionary using date as the key and prcp as the value.


#Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(prcp_scores)

#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    return jsonify(station_count)

#Query the dates and temperature observations of the most active station for the last year of data
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
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
    
