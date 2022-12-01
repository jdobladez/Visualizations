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

# use https://www.kaggle.com/code/nguyenthicamlai/aribnb-preprocessing-eda


app = Dash(__name__)

# Loading Data

df = pd.read_csv(
    '/home/julia/Documents/TUE/Year 2/Quartile 2/Visualizations/Data Sets/Airbnb/airbnb_open_data.csv',
    low_memory=False)

# Cleaning Data

df.drop(columns=["country code", "country"], axis=1, inplace=True)

df = df.dropna(subset=['host_identity_verified'])

# these two columns do no change as it is always the same city

def remove_dollar_sign(value):
    if pd.isna(value):
        return np.NaN
    else:
        return float(value.replace("$", "").replace(",", "").replace(" ", ""))


df["price"] = df["price"].apply(lambda x: remove_dollar_sign(x))

df["service fee"] = df["service fee"].apply(lambda x: remove_dollar_sign(x))

df["last review"] = pd.to_datetime(df["last review"])

fig = px.scatter(data_frame=df, x="price", y="review rate number", color="host_identity_verified")
fig.show()

app.layout = html.Div(children=[
    dcc.Graph(
        id='graph',
        figure=fig
    )
])

if __name__ == '__scratch__':
    app.run_server(debug=False, dev_tools_ui=False)

