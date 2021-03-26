### Step 2 Climate App ###

# Import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# Import Flask
from flask import Flask, jsonify

#### Database Setup ###
engine = create_engine("sqlite:///hawaii.sqlite")
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
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"      
        f"JSON list of stations from the dataset:<br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"JSON list of temperature observations (TOBS) for previous year:<br/>"
        f"<a href='/api/v1.0/tobs'>TOBS</a><br/>"
        f"Return JSON list of minimum, average, and max temperature for given start or start-end range:<br/>"
        f"<a href='/api/v1.0/<start>/<end>'>min, avg, max temp</a><br/>"
        f"Calculate TMIN, TAVG, and TMAX for all dates greater or equal to start date:<br/>"
        f"<a href='/api/v1.0/<start>'>TMIN, TAVG, TMAX start date only</a><br/>"
        f"Calculate TMIN, TAVG, and TMAX for dates between start and end dates:<br/>"
        f"<a hreaf='/api/v1.0/<start>'>TMIN, TAVG, TMAX between start/end date</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session link from Python to DB
    session = Session(engine)  
    # Query last year of preciptation and query results 
    last_year_date=dt.date(2017, 8, 23) - dt.timedelta(days=366)
    results = session.query(measurement.date,func.max(measurement.prcp))\
        .filter(func.strftime('%Y-%m-%d',measurement.date) > last_year_date)\
        .group_by(measurement.date).all()
    # End session
    session.close()
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    prcp_scores = []
    for year_prcp in results:
        year_prcp_dict = {}
        year_prcp_dict["Date"] = year_prcp.date
        year_prcp_dict["Precipitation"] = year_prcp.prcp
        prcp_scores.append(prcp_dict)
    #Return the JSON representation of your dictionary
    return jsonify(prcp_scores)
    
#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    # Create session link
    #session = Session(engine)
    # Query all stations
    results = session.query(station).all()
    #session.close()
    # Create dictionary from row data and append to list
    stations = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        stations.append(station_dict)
    return jsonify(stations)
    #session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    #Query the dates and temperature observations of the most active station for the last year of data
    session = Session(engine)
    last_year_date=dt.date(2017, 8, 23) - dt.timedelta(days=366)
    results = session.query(measurement.tobs).filter(measurement.station == "USC00519281")\
        .filter(measurement.date >= last_year_date).all()
    # Create dictionary 
    year_tobs = []
    for tobs in results:
        tobs_dict = {}
        tobs_dict["Date"] = tobs.date
        tobs_dict["Temperature"] = tobs.tobs
        year_tobs.append(tobs_dict)
    session.close()
    #Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(year_tobs)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#@app.route("/api/v1.0/<start>")
#def active_station():

    #return jsonify(active_station)

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
#@app.route("/api/v1.0/<start>/<end>")
#def station():

    #return jsonify(station)

if __name__ =="__main__":
    app.run(debug=True)
    
