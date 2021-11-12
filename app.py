import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)




# Flask Setup

app = Flask(__name__)


# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes Below:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/<start><br/>"
        f"Put the start date in 'YYYY-MM-DD' format<br/>"
        f"<br/>"
        f"/api/v1.0/<start>/<end><br/>"   
        f"Put the dates in 'YYYY-MM-DD/YYYY-MM-DD' format<br/>"
        )  

@app.route("/api/v1.0/precipitation")
def precipitation():

    
    rain = session.query(Measurements.date, Measurements.prcp).\
        order_by(Measurements.date).all()

    rain_totals = []
    for row in rain:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        rain_totals.append(row)

    return jsonify(rain_totals)

@app.route("/api/v1.0/stations")
def stations():
    
    station_info = session.query(Station.name).all()
    station_info2 = session.query(Station.station).all()
    x=0
    full_station_info = []
    for row in station_info:
        row = {}
        row["station id"] = station_info[x]
        row["station name"] = station_info2[x]
        full_station_info.append(row)
        x += 1

    return jsonify(full_station_info)

@app.route("/api/v1.0/tobs")
def tobs():
    
    temp1 = session.query(Measurements.date).\
        filter(Measurements.date <= '2017-08-23').\
        filter(Measurements.date >= '2016-08-23').\
        order_by(Measurements.date).all()
    
    temp2 = session.query(Measurements.tobs).\
        filter(Measurements.date <= '2017-08-23').\
        filter(Measurements.date >= '2016-08-23').\
        order_by(Measurements.date).all()
    y=0
    temperature_data = []
    for row in temp1:
        row = {}
        row["date"] = temp1[y]
        row["tobs"] = temp2[y]
        temperature_data.append(row)
        y += 1

    return jsonify(temperature_data)
    
@app.route("/api/v1.0/<start>")
def start_stats(start):
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = start_date + dt.timedelta(days=365)
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
              filter(Measurements.date >= start_date).\
              filter(Measurements.date <= end_date).\
              order_by(Measurements.date.desc()).all()
    
    for stats in results:
        stats = {"Min Temp":results[0][0],"Avg Temp":results[0][1],"Max Temp":results[0][2]}
        
    return jsonify(stats) 

@app.route("/api/v1.0/<start>/<end>")
def tstartend(start,end):         
   
    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs),func.max(Measurements.tobs)).\
                  filter(Measurements.date >= start, Measurements.date <= end).order_by(Measurements.date.desc()).all()

    for temps in results:
        dict = {"Minimum Temp":results[0][0],"Average Temp":results[0][1],"Maximum Temp":results[0][2]}
    return jsonify(dict)   


if __name__ == '__main__':
    app.run(debug=True)