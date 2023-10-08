import model as model
import sqlite3
from flask import Flask, render_template, request, g, jsonify
import pandas as pd
import numpy    as np

import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt # matplotlib

app = Flask(__name__)


# Sqlite3 code
DATABASE = 'data/userip.db'
MAP_KEY = "c4f9c87a128b458b6a69d96cfc2e3e60"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False, commit=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if commit:
        get_db().commit()
    return (rv[0] if rv else None) if one else rv


def update_db(req, table=None):
    if table is not None:
        if table == 'report':
            query_db(
                f"CREATE TABLE IF NOT EXISTS {table} (message TEXT)")
        else:
            query_db(
                f"CREATE TABLE IF NOT EXISTS {table} (name TEXT, email TEXT, feedback TEXT)")

        # Insert data into database
        if table == 'feedback':
            query_db(
                    f"INSERT INTO {table} (name, email, feedback) VALUES (?, ?, ?)",
                    (req.form.get('fd-name'), req.form.get('fd-email'), req.form.get('fd-message')), commit=True)
        elif table == 'report':
            query_db(
                    f"INSERT INTO {table} (message) VALUES (?)",
                    (req.form.get('rprt-message')), commit=True)



# data visualization
def pie_areas():
    
    cntr = ["ITA", "ARG", "SPA", "USA", "IND"]
    cntrn = ["Italy", "Argentina", "Spain", "USA", "India"]
    areas = []
    for c in cntr:
        df = pd.read_csv(f'https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{c}/1/')
        areas.append(calculate_damaged_area_coordinates(df['latitude'], df['longitude']))

    plt.pie(np.array(areas), labels=cntrn)
    plt.savefig(f'static/images/area.png')



def pie_frp():
    
    countries = ["ITA", "ARG", "USA", "IND", "ESP"]
    countries_n = ["Italy", "Argentina", "United States of America", "India", "Spain"]
    MAP_KEY = 'c4f9c87a128b458b6a69d96cfc2e3e60'

    frp = []

    for c in countries:

        df = pd.read_csv(f'https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{c}/1/')
        col = df['frp']
        cm = col.mean()
        cm = f"{cm:.3f}"
        cm = float(cm)
        frp.append(cm)

        y = np.array(frp)
        print(y)

        # Create the Pie Chart
        plt.pie(y, labels=countries_n, autopct='%1.1f%%', startangle=140)

        # Customize the Pie Chart
        plt.title('FRP')
        plt.axis('equal')
        # plt.legend()

        # Display the Chart
        plt.show()
        plt.savefig("{{ url_for('static', '/images/frp.png') }}", transparent=True)



def pie_bti4():
    
    cntr = ["ITA", "ARG", "SPA", "USA", "IND"]
    cntrn = ["Italy", "Argentina", "Spain", "USA", "India"]
    bti4 = []
    for c in cntr:
        df = pd.read_csv(f'https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{c}/1/')
        bti4.append(df['bright_ti4'].mean())

    plt.pie(np.array(bti4), labels=cntrn)
    plt.savefig(f'static/images/bti4.png')


# data fetching"]

def calculate_damaged_area_coordinates(latitude, longitude):
    # Create a Polygon object from latitudes and longitudes
    damaged_area_polygon = Polygon(zip(longitude, latitude))

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(geometry=[damaged_area_polygon])
    # Set the Coordinate Reference System (CRS) to WGS 84
    gdf.crs = "EPSG:4326"

    # Calculate the damaged area in square degrees
    damaged_area_square_degrees = gdf.geometry.area.values[0]
    
    return damaged_area_square_degrees




# app routes
@app.route('/', methods=['GET', 'POST'])
def index():

    pie_areas()
    pie_bti4()
    pie_frp()
    
    return render_template('index.html', title='Fire Forecasters')







# @app.route('/get_area')
# def get_area():
#     return areas

@app.route('/get_frp')
def get_frp():
    cntr = ["ITA", "ARG", "SPA", "USA", "IND"]
    frp = []
    for c in cntr:
        url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{c}/1/"
        data = pd.read_csv(url)
        frp.append(data['frp'].mean())

    return jsonify({"frp": frp})















@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        if 'fd-message' in request.form.keys():
            update_db(request, table='feedback')
            return render_template('feedback_success.html', title='Feedback')
        elif 'rprt-message' in request.form:
            update_db(request, table='report')
            return render_template('index.html', title='Fire Forecasters')
        
    return render_template('feedback.html', title='Feedback')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')


@app.route('/emergency', methods=['GET', 'POST'])
def emergency():
    return render_template('emergency.html', title='Emergency Catalogue')




















if __name__ == '__main__':
    app.run(debug=True)
