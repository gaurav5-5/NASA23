# import libraries
from flask import jsonify, request

import requests # https
import pandas as pd #dataframe
import numpy as np
import math

#geopandas
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt # matplotlib

# Globals:
MAP_KEY = "c4f9c87a128b458b6a69d96cfc2e3e60"
countries = []

# get fire data from NASA
def fetch_fire_data():
    url="https://firms.modaps.eosdis.nasa.gov/api/area/csv/c4f9c87a128b458b6a69d96cfc2e3e60/VIIRS_SNPP_NRT/-85,-57,-32,14/1/2023-10-08"
    response = requests.get(url)

    if response.status_code == 200:
        data = pd.read_csv(url)
        print(data.head())
        return data
    else:
        print("Failed to fetch data.")
        return None
    
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


# visulaize fire data on map
def visualize_fire_data_on_map(data):
    gdf = gpd.GeoDataFrame(data,
                           geometry=gpd.points_from_xy(data.longitude, data.latitude))

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    fig, ax = plt.subplots(figsize=(10, 6))
    world.boundary.plot(ax=ax, linewidth=1, color='gray')
    gdf.plot(ax=ax, markersize=5, color='red', label='Fire Incidents')

    plt.title('Fire Incidents on Map')
    plt.legend()
    plt.show()

def graph_datas(name, key=MAP_KEY):
    try:
        dates = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
        dfc = []
        for date in dates:
            url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{key}/VIIRS_SNPP_NRT/{name}/1/{date}"
            dfc.append(pd.read_csv(url))

        damage_areas = []

        for df in dfc:
            area = calculate_damaged_area_coordinates(df['latitude'], df['longitude'])
            damage_areas.append(area)

        fig,ax1 = plt.subplots()

        fire_incidents = [5,7,6,8,5]

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Damage Area (sq km)', color='tab:blue')
        ax1.plot(dates, damage_areas, color='tab:blue', marker='o', label='Damage Area')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.set_xticklabels(dates, rotation=45)  # Rotate x-axis labels for readability

        # Create a second y-axis for fire incidents

        # Add legends for both datasets
        lines, labels = ax1.get_legend_handles_labels()
        ax1.legend(lines, labels , loc='upper right')

        # Set a title and display the plot
        plt.title('Damage Area over Time')
        plt.tight_layout()
        plt.show()
    except:
        pass


def get_area():
    cntr = ["ITA", "ARG", "SPA", "USA", "IND"]
    cntrn = ["Italy", "Argentina", "Spain", "USA", "India"]
    areas = []
    for c in cntr:
        try:
            url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{c}/1/"
            data = pd.read_csv(url)
            calc = calculate_damaged_area_coordinates(data['latitude'], data['longitude'])
            areas.append(calc)
        except:
            pass

    return jsonify({"area": areas})

def get_frp():
    cntr = ["ITA", "ARG", "SPA", "USA", "IND"]
    cntrn = ["Italy", "Argentina", "Spain", "USA", "India"]
    frp = []
    for c in cntr:
        url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{c}/1/"
        data = pd.read_csv(url)
        frp.append(data['frp'].mean())

    return jsonify({"frp": frp})


def get_bti4():
    cntr = ["ITA", "ARG", "SPA", "USA", "IND"]
    cntrn = ["Italy", "Argentina", "Spain", "USA", "India"]
    bti4 = []
    for c in cntr:
        url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{MAP_KEY}/VIIRS_SNPP_NRT/{c}/1/"
        data = pd.read_csv(url)
        bti4.append(data['bright_ti4'].mean())

    return jsonify({"bti4": bti4})



# Main function
if __name__ == '__main__':
    # Simulate fetching NASA's fire data
    # fire_data = fetch_fire_data()
    # reads countries
    cname = "IND"
    countries = pd.read_json('https://firms.modaps.eosdis.nasa.gov/api/countries/?format=json')
    print(countries['geom'])


    #     # if processed_data['frp'][0] > 0.8:
    #     #     sender_email = "adi004gupta@gmail.com"
    #     #     sender_password = "helloadi77"
    #     #     receiver_email = "khushey7thakur@gmail.com

    #         # send_email_alert(sender_email, sender_password, receiver_email)

    #     # Visualize fire data on a map
    #     # visualize_fire_data_on_map(processed_data)