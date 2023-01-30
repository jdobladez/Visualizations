import dash
from main import app
from dash import Dash, html, dcc, Input, Output
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
df['neighbourhood_group'] = df['neighbourhood_group'].replace(['Staten Island'], 'Staten_Island')
df = df[df["neighbourhood_group"].notna()]
df["price"] = df["price"].apply(lambda x: remove_dollar_sign(x))
df["service_fee"] = df["service_fee"].apply(lambda x: remove_dollar_sign(x))
df["host_identity_verified"] = df["host_identity_verified"].apply(lambda x: no_values(x))

df["country"] = df["country"].apply(lambda x: no_values(x))
df["cancellation_policy"] = df["cancellation_policy"].apply(lambda x: no_values(x))
df["last_review"] = df["last_review"].apply(lambda x: no_values(x))
df["calculated_host_listings_count"] = df["calculated_host_listings_count"].apply(lambda x: no_values(x))
df["license"] = df["license"].apply(lambda x: no_values(x))

Brooklyn = df[df["neighbourhood_group"]=="Brooklyn"].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)
Manhattan = df[df["neighbourhood_group"]=="Manhattan"].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)
Queens = df[df["neighbourhood_group"]=="Queens"].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)
Staten_Island = df[df["neighbourhood_group"]=="Staten_Island"].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)
Bronx = df[df["neighbourhood_group"]=="Bronx"].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)

trial = df.filter(['price', 'lat', 'long', 'id'], axis=1)


maps =  px.scatter_mapbox(df, lat="lat", lon="long", color="neighbourhood_group",
                            color_continuous_scale=px.colors.sequential.tempo, mapbox_style="stamen-terrain", zoom = 10,
                          height=20, width=5)

brooklyn_map = px.density_mapbox(Brooklyn, "lat", "long", z="price", mapbox_style="stamen-terrain")

heatmap = px.scatter_mapbox(df, lat="lat", lon="long", color="price",
                            color_continuous_scale=px.colors.sequential.tempo, mapbox_style="stamen-terrain", zoom = 10)


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
    ]),
    html.Div([
        html.H4('Neighbourhood listing analysis'),
        html.P("Select a neighbourhood group:"),
        dcc.RadioItems(
            id='neighbourhood_group',
            options=['Brooklyn', 'Manhattan', 'Queens', 'Staten_Island', 'Bronx'],
            value="Manhattan",
            inline=True
        ),
        dcc.Graph(id="graph")])
])

@app.callback(
    Output("graph", "figure"),
    Input("neighbourhood_group", "value"))
def display_histogram(neighbourhood_group):
    data = df[df["neighbourhood_group"]==neighbourhood_group].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)
    fig = px.histogram(data, x="neighbourhood", y="availability_365", color="room_type",
                       marginal="box", barmode="group", # or violin, rug
                       histfunc='avg', cumulative=False,histnorm=None, color_discrete_sequence=['rgb(229, 134, 6)','rgb(93, 105, 177)','rgb(165, 170, 153)','rgb(36, 121, 108)'], hover_data=data.columns)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
