import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/<start_date><br/>"
        f"/api/v1.0/start_end_date/<start_date>/<end_date><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns the dates and temperature observations from the last year"""
    # Calculate the date 1 year ago from max date in dataset
    date_year_ago=dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    tobs_data=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>date_year_ago).all()

    # Convert the query results to a Dictionary
    tobs_data_dict = dict(tobs_data)

    return jsonify(tobs_data_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Returns all the stations"""
    # Perform a query to retrieve the stations
    stations_data=session.query(Station.station,Station.name).distinct().all()

    # Convert the query results to a Dictionary
    stations_data_list = list(stations_data)

    return jsonify(stations_data_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Returns the temperature observations from the last year"""
    # Calculate the date 1 year ago from max date in dataset
    date_year_ago=dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    tobs_data=session.query(Measurement.tobs).filter(Measurement.date>date_year_ago).all()

    # Convert the query results to a Dictionary
    tobs_data_list = list(tobs_data)

    return jsonify(tobs_data_list)

@app.route("/api/v1.0/start_date/<start_date>")
def start_date(start_date):
    """Returns the Tmin, Tavg and Tmax for all dates greater than and equal to the start date"""
    # Perform a query to retrieve the Tmin, Tavg and Tmax for all dates greater than and equal to the start date
    dates=session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ).filter(Measurement.date==start_date).all()
    
    if None in dates[0]:
        return jsonify({"error": f"Date: {start_date} not found."})
    return jsonify(dates)
    
@app.route("/api/v1.0/start_end_date/<start_date>/<end_date>")
def start_end_date(start_date,end_date):
    """Returns the Tmin, Tavg and Tmax for all dates between start and end dates"""
    # Perform a query to retrieve the Tmin, Tavg and Tmax for all dates between start and end dates
    dates=session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
    ).filter(Measurement.date>=start_date).filter(Measurement.date<=end_date).all()
    
    if None in dates[0]:
        return jsonify({"error": f"Dates not found."})
    return jsonify(dates)
        
if __name__ == '__main__':
    app.run(debug=True)

