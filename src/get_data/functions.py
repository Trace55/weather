import pandas as pd
import plotly.express as px
from geopy.distance import geodesic
from datetime import datetime, date
from meteostat import Point, Daily, Stations
import os

# Import Meteostat library
from meteostat import Stations


def get_all_data():
    unprocessed_data = {}

    unprocessed_data['daily_weather'] = get_daily_weather(1000, datetime(2018, 1, 1), datetime(2025, 12, 31))

    return unprocessed_data



def get_daily_weather(points, start, end):
    """
    This function assumes you have a github_data dir in the same dir as github

    """

    current_directory = os.getcwd()
    write_out_path = ('/').join(current_directory.split('/')[:3]) + r'/github_data/weather/daily_weather.csv'

    try:
        
        daily_weather = pd.read_csv(write_out_path)
        print('File found, pulling from local file')
    except:
        print('Running Api pull')

        stations = Stations()
        # random point in the middle of iowa
        stations = stations.nearby(42.1133, -93.526)
        # pull closest 1000 stations data
        station = stations.fetch(points)

        daily_weather = pd.DataFrame()

        for i, row in station.iterrows():
        
            pull_point = Point(row['latitude'],row['longitude'] )

            # Get daily data for 2018
            data = Daily(pull_point, start, end)
            data = data.fetch()
            data['name'] = row['name']
            data['lat'] = row['latitude']
            data['lon'] = row['longitude']
            data['date_pulled'] = date.today()


            daily_weather = pd.concat([daily_weather,data])

        daily_weather = daily_weather.reset_index().rename(columns = {'index':'date'})
        
        daily_weather.to_csv(write_out_path)

    return daily_weather
