from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
# Python SQL toolkit and Object Relational Mapper
from sqlalchemy import create_engine, and_, inspect, func
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

start_date='2011-02-28'
end_date='2012-02-28'

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    # """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation entries by date: /api/v1.0/precipitation<br/>"
        f"Return a JSON list of stations from the dataset: /api/v1.0/stations<br/>"
        f"Return a JSON list of Temperature Observations (tobs) for the previous year: /api/v1.0/tobs<br/>"   
        f"Minimum temperature (1), average temperature (2), and maximum temperature (3) for dates after {start_date}: /api/v1.0/{start_date}<br/>"
        f"Minimum temperature (1), average temperature (2), and maximum temperature (3) for dates {start_date} to {end_date}: /api/v1.0/{start_date}/{end_date}<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    first_row_m = session.query(Measurement).first()
    first_row_m.__dict__
    # Exploratory Climate Analysis
    inspector = inspect(engine)
    columns = inspector.get_columns('measurement')
    first_row_s = session.query(Station).first()
    first_row_s.__dict__
    # Exploratory Climate Analysis
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    # Calculate the date 1 year ago from the last data point in the database
    # Latest Date
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_day = dt.datetime.strptime(last_day[0], '%Y-%m-%d')
    print("Last Date: ", last_day)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    print("Query Date: ", query_date)
    measurements = session.query(Measurement)
    # Perform a query to retrieve the data and precipitation scores
    year_query = measurements.filter(and_(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23')) 
    # for day in year_query:
    #     print(day.prcp, day.date)
    year_query = session.query(Measurement.date, Measurement.prcp).filter(and_(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23')).all()
    df = pd.DataFrame(year_query, columns=['date', 'precipitation'])
    df.set_index(df['date'], drop=True, inplace=True)
    # Sort the dataframe by date
    df.sort_values(by="date", inplace=True, ascending=True)
    # Use Pandas Plotting with Matplotlib to plot the data
    date=df['date']
    prcp=df['precipitation']
    prcp_dict = dict(zip(df['date'], df['precipitation']))
    return jsonify(prcp_dict)



@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    station=session.query(Measurement.station).distinct().all()
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    active= session.query(Measurement.station, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').all()
    sel = [func.min(Measurement.tobs),
       func.max(Measurement.tobs),
       func.avg(Measurement.tobs)]
    top_stn_results = session.query(*sel).\
    filter(Measurement.station == 'USC00519281').all()
    # Choose the station with the highest number of temperature observations.
    stations=session.query(Measurement.station, Measurement.tobs).all()
    unique=(session.query(Measurement.station).distinct())
    for u in unique:
        print("(", u.station, ",", session.query(Measurement.tobs).filter_by(station=u.station).count(), ")")
    return jsonify(stations)

def calc_temps(start_date, end_date):
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

@app.route(f"/api/v1.0/{start_date}/{end_date}")
def start_end():
    print(calc_temps(start_date, end_date))
    trip=calc_temps(start_date, end_date)
    session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    return jsonify(trip)

    #print(f"Minimum temperature (1), average temperature (2), and maximum temperature (3) for dates {start_date} to {end_date} {jsonify(trip)}" 

# @app.route(f"/api/v1.0/{start_date}")



if __name__ == '__main__':
    app.run(debug=True)



