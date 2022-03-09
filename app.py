from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from sqlalchemy import desc
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)
###
year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
year_ago

start_date = dt.datetime(2016,8,23)

precipitation_dates = []
precipitation_scores = []
for row in session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > start_date).all():
    precipitation_dates.append(row[0])
    precipitation_scores.append(row[1])
###
active_stations = []

for row in session.execute('SELECT station, COUNT(station) AS count FROM measurement GROUP BY station ORDER BY count DESC'):
    active_stations.append(row)

most_active = active_stations[0][0]
###
stations_list = []
for station in session.query(Station.station):
    stations_list.append(station)
stations_list
###
last_12_months = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.date > start_date, Measurement.station == most_active)

dates = []
temp = []

for row in last_12_months:
    #print(row)
    dates.append(row[0])
    temp.append(row[2])
###
precipitation_dict = {precipitation_dates[i]: precipitation_scores[i]\
    for i in range(0, len(precipitation_dates))}
temperature_dict = {dates[i]: temp[i]\
    for i in range(0, len(dates))}
###
@app.route("/")
def home():
    return(
        f"All available routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def station():
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(temperature_dict)

@app.route("/api/v1.0/<start>")
def start_search(start):
    temps = []
    for day in temperature_dict:
        if day >= start:
            temps.append(temperature_dict[day])
    
    return (f"Mean Temp: {sum(temps)/len(temps)} <br>Max Temp:{max(temps)} <br>Min Temp:{min(temps)}")

@app.route("/api/v1.0/<start>/<end>")
def end_search(start, end):
    temps = []
    for day in temperature_dict:
        if day >= start and day <= end:
            temps.append(temperature_dict[day])
    
    return (f"Mean Temp: {sum(temps)/len(temps)} <br>Max Temp:{max(temps)} <br>Min Temp:{min(temps)}")

if __name__ == "__main__":
    app.run(debug=True)