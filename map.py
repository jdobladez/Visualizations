import dash
from main import app
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import missingno as msno

# Create graphs
df = pd.read_csv(
    '/home/julia/Documents/TUE/Year 2/Quartile 2/Visualizations/Data Sets/Airbnb/airbnb_open_data.csv', low_memory=False)


# Cleaning Data
def remove_dollar_sign(value):
    if pd.isna(value):
        return np.NaN
    else:
        return float(value.replace("$", "").replace(",", "").replace(" ", ""))


def no_values(val):
    if pd.isna(val):
        return np.NaN


df.columns = [col.lower().replace(" ", "_") for col in df.columns]

df['neighbourhood_group'] = df['neighbourhood_group'].replace(['brookln'], 'Brooklyn')
df['neighbourhood_group'] = df['neighbourhood_group'].replace(['manhatan'], 'Manhattan')
df["price"] = df["price"].apply(lambda x: remove_dollar_sign(x))
df["service_fee"] = df["service_fee"].apply(lambda x: remove_dollar_sign(x))
df["host_identity_verified"] = df["host_identity_verified"].apply(lambda x: no_values(x))
df["neighbourhood"] = df["neighbourhood"].apply(lambda x: no_values(x))
df["country"] = df["country"].apply(lambda x: no_values(x))
df["cancellation_policy"] = df["cancellation_policy"].apply(lambda x: no_values(x))
df["last_review"] = df["last_review"].apply(lambda x: no_values(x))
df["calculated_host_listings_count"] = df["calculated_host_listings_count"].apply(lambda x: no_values(x))
df["license"] = df["license"].apply(lambda x: no_values(x))

brooklyn = df[df["neighbourhood_group"] == "Brooklyn"].filter(['price', 'lat', 'long', 'id'], axis=1)
trial = df.filter(['price', 'lat', 'long', 'id'], axis=1)

maps = px.scatter(trial, "lat", "long", color="price")

brooklyn_map = px.density_mapbox(brooklyn, "lat", "long", z="price", mapbox_style="stamen-terrain")

heatmap = px.density_heatmap(trial, "lat", "long", "price")

# Create app layout

app.layout = html.Div([
    html.Div([
        html.H1("This is a trial"),
        html.P("Please work"),
    ]),
    html.Div([
        html.Div([dcc.Graph(figure=maps),
                  dcc.Graph(figure=brooklyn_map)]),
        html.Div([dcc.Graph(figure=heatmap)])
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
