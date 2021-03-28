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
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"      
        f"JSON list of stations from the dataset:<br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"JSON list of temperature observations (TOBS) for previous year:<br/>"
        f"<a href='/api/v1.0/tobs'>TOBS</a><br/>"
        f"Return JSON list of minimum, average, and max temperature for given start or start-end range:<br/>"
        f"<a href='/api/v1.0/<start>/<end>'>Min, Avg, Max Temp</a><br/>"
        f"Calculate TMIN, TAVG, and TMAX for all dates greater or equal to start date:<br/>"
        f"<a href='/api/v1.0/<start>'>TMIN, TAVG, TMAX start date only</a><br/>"
        f"Calculate TMIN, TAVG, and TMAX for dates between start and end dates:<br/>"
        f"<a hreaf='/api/v1.0/<start>'>TMIN, TAVG, TMAX between start/end date</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query last year of preciptation and query results 
    last_year_date=dt.date(2017, 8, 23) - dt.timedelta(days=366)
    results = session.query(measurement.date,func.max(measurement.prcp)).filter(func.strftime('%Y-%m-%d',measurement.date) > last_year_date).group_by(measurement.date).all()
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    prcp_scores = []
    for year_prcp in results:
        year_prcp_dict = {"Date": year_prcp[0], "Precipitation": year_prcp[1]}
        prcp_scores.append(year_prcp_dict)
    #Return the JSON representation of your dictionary
    return jsonify(prcp_scores)
    
#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(station.station).all()
    print(results)
    # Create dictionary from row data and append to list using np.ravel of results
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #Query the dates and temperature observations of the most active station for the last year of data
    last_year_date=dt.date(2017, 8, 23) - dt.timedelta(days=366)
    #results = session.query(measurement[3]).filter(measurement.date == "USC00519281").filter(measurement[1] >= last_year_date).all()
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == "USC00519281").filter(measurement.date >= last_year_date).all()
    print(results)
    # Create dictionary 
    year_tobs_data = []
    for year_tobs in results:
        year_tobs_dict = {"Date": year_tobs[0], "Temperature": year_tobs[1]}
        year_tobs_data.append(year_tobs_dict)
    # #Return a JSON list of temperature observations (TOBS) for the previous year.
    return jsonify(year_tobs)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
##@app.route("/api/v1.0/<start>")
#def active_station():
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))
    return jsonify(active_station)

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
#@app.route("/api/v1.0/<start>/<end>")
#def station():

    #return jsonify(station)

# Close session
session.close()

if __name__ =="__main__":
    app.run(debug=True)
    
