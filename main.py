from flask import Flask, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

raw_data = pd.read_csv("data_small/stations.txt", skiprows=17)
station_data = raw_data[['STAID','STANAME                                 ']]

@app.route("/")
def home():
    return render_template("home.html", data=station_data.to_html())


@app.route("/api/v1/<station>/<date>")
def get_temperature(station, date):
    location = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(location, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze()/10
    print(temperature)
    return {'station':station, 'date': date,
            'temperature':temperature}

@app.route("/api/v1/<station>")
def get_station_records(station):
    location = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(location, skiprows=20, parse_dates=["    DATE"])
    return df.to_dict(orient="records")


@app.route("/api/v2/<station>/<year>")
def get_year_data(station, year):
    location = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    df = pd.read_csv(location, skiprows=20, parse_dates=["    DATE"])
    df["YEAR"] = df["    DATE"].apply(lambda x: x.year)

    yearly_data = df[df["YEAR"] == int(year)]
    print(df.head(15))
    return yearly_data.to_dict(orient="records")

if __name__== "__main__":
    app.run(debug=True)