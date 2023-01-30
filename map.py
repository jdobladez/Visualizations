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

def rem_outliers(col):
    q25 = df[col].quantile(q=0.25)
    q75 = df[col].quantile(q=0.75)
    intr_qr = q75-q25
    maxi = q75+(1.5*intr_qr)
    mini = q75-(1.5*intr_qr)
    if col == "minimum_nights":
        mini = 1
    elif col == "availability_365":
        mini = 0
        maxi = 365
    elif col == "lat":
        return
    elif col == "long":
        return
    elif col == "id":
        return
    df.drop(df.loc[df[col] > maxi].index, inplace=True)
    df.drop(df.loc[df[col] < mini].index, inplace=True)
    return

df.columns = [col.lower().replace(" ", "_") for col in df.columns]
df.drop(df.loc[df['availability_365'] > 365].index, inplace=True)
df.drop(df.loc[df['availability_365'] < 0].index, inplace=True)
df.dropna(subset=['neighbourhood'], inplace=True)
df['neighbourhood_group'] = df['neighbourhood_group'].replace(['brookln'], 'Brooklyn')
df['neighbourhood_group'] = df['neighbourhood_group'].replace(['manhatan'], 'Manhattan')
df['neighbourhood_group'] = df['neighbourhood_group'].replace(['Staten Island'], 'Staten_Island')
df = df[df["neighbourhood_group"].notna()]
df["price"] = df["price"].apply(lambda x: remove_dollar_sign(x))
df["service_fee"] = df["service_fee"].apply(lambda x: remove_dollar_sign(x))
df.drop_duplicates(subset=['lat','long'])
rem_outliers("minimum_nights")
rem_outliers("price")
rem_outliers("number_of_reviews")
rem_outliers("review_rate_number")
rem_outliers("calculated_host_listings_count")
rem_outliers("reviews_per_month")
rem_outliers("availability_365")

Brooklyn = df[df["neighbourhood_group"]=="Brooklyn"].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)
trial = df.filter(['price', 'lat', 'long', 'id'], axis=1)

''''

Manhattan = df[df["neighbourhood_group"]=="Manhattan"].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)
Queens = df[df["neighbourhood_group"]=="Queens"].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)
Staten_Island = df[df["neighbourhood_group"]=="Staten_Island"].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)
Bronx = df[df["neighbourhood_group"]=="Bronx"].filter(['price','lat', 'long', 'id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)

 html.Div([dcc.Graph(figure=maps), dcc.Graph(figure=brooklyn_map)]),
 
 
maps =  px.scatter_mapbox(df, lat="lat", lon="long", color="neighbourhood_group",
                            color_continuous_scale=px.colors.sequential.tempo, mapbox_style="stamen-terrain", zoom = 10)

brooklyn_map = px.density_mapbox(Brooklyn, "lat", "long", z="price", mapbox_style="stamen-terrain")
'''''


scatter = px.scatter_mapbox(df, lat="lat", lon="long", color="price",
                            color_continuous_scale=px.colors.sequential.tempo, mapbox_style="stamen-terrain",
                            zoom=10)

all_neighbourhoods = {
    'Brooklyn': ['Williamsburg', 'Windsor Terrace', 'Bedford-Stuyvesant',
       'Flatbush', 'South Slope', 'Prospect-Lefferts Gardens',
       'Clinton Hill', 'Park Slope', 'Brooklyn Heights',
       'Prospect Heights', 'Flatlands', 'Greenpoint', 'Cobble Hill',
       'Fort Greene', 'Kensington', 'Crown Heights', 'Carroll Gardens',
       'Gowanus', 'Bushwick', 'Boerum Hill', 'Gravesend',
       'Brighton Beach', 'Cypress Hills', 'Bay Ridge', 'Vinegar Hill',
       'East New York', 'Sunset Park', 'Columbia St', 'Canarsie',
       'Borough Park', 'Downtown Brooklyn', 'Midwood', 'Bensonhurst',
       'Fort Hamilton', 'Sheepshead Bay', 'Red Hook', 'East Flatbush',
       'DUMBO', 'Sea Gate', 'Brownsville', 'Navy Yard', 'Manhattan Beach',
       'Dyker Heights', 'Bergen Beach', 'Coney Island', 'Bath Beach',
       'Mill Basin', 'Gerritsen Beach'],

    'Manhattan': ['Harlem', 'Upper West Side', 'East Harlem', 'Inwood', 'Kips Bay',
       'Lower East Side', 'Upper East Side', 'East Village',
       "Hell's Kitchen", 'Chelsea', 'West Village', 'Roosevelt Island',
       'Greenwich Village', 'Little Italy', 'Midtown', 'SoHo',
       'Morningside Heights', 'Nolita', 'NoHo', 'Tribeca',
       'Chinatown', 'Gramercy', 'Financial District',
       'Washington Heights', 'Flatiron District', 'Battery Park City',
       'Two Bridges', 'Civic Center', 'Murray Hill', 'Theater District',
       'Stuyvesant Town', 'Marble Hill'],

    'Queens': ['Jamaica', 'Ditmars Steinway', 'Astoria', 'Forest Hills',
       'Elmhurst', 'Jackson Heights', 'St. Albans', 'Rego Park',
       'Long Island City', 'Briarwood', 'Ozone Park', 'Sunnyside',
       'Arverne', 'Ridgewood', 'Cambria Heights', 'Woodside', 'Bayside',
       'Flushing', 'Kew Gardens', 'College Point', 'Richmond Hill',
       'Glendale', 'Queens Village', 'Bellerose', 'Maspeth',
       'Kew Gardens Hills', 'Bay Terrace', 'Whitestone', 'Bayswater',
       'Fresh Meadows', 'Rockaway Beach', 'East Elmhurst', 'Woodhaven',
       'Corona', 'Middle Village', 'Jamaica Estates',
       'Springfield Gardens', 'Howard Beach', 'Holliswood', 'Rosedale',
       'Far Rockaway', 'Edgemere', 'Belle Harbor', 'South Ozone Park',
       'Jamaica Hills', 'Hollis', 'Douglaston', 'Neponsit', 'Laurelton',
       'Breezy Point', 'Little Neck'],

    'Staten_Island': ['Emerson Hill', 'Shore Acres', 'Clifton', 'Graniteville',
       'Tottenville', 'Tompkinsville', 'Mariners Harbor', 'St. George',
       'Woodrow', 'Concord', 'Lighthouse Hill', 'Stapleton',
       'Great Kills', 'Dongan Hills', 'Randall Manor',
       'Castleton Corners', 'Midland Beach', 'Richmondtown',
       'Howland Hook', 'New Dorp Beach', "Prince's Bay", 'South Beach',
       'Eltingville', 'Oakwood', 'Arrochar', 'West Brighton',
       'Grant City', 'Port Richmond', 'Westerleigh',
       'Bay Terrace, Staten Island', 'Fort Wadsworth', 'New Springville',
       'Arden Heights', "Bull's Head", 'New Dorp', 'Rossville',
       'Willowbrook', 'New Brighton', 'Grymes Hill', 'Rosebank',
       'Huguenot', 'Todt Hill', 'Chelsea, Staten Island', 'Silver Lake'],

    'Bronx': ['Wakefield', 'Spuyten Duyvil', 'Longwood', 'Allerton', 'Fieldston',
       'City Island', 'Concourse', 'Kingsbridge', 'Williamsbridge',
       'Soundview', 'Parkchester', 'Bronxdale', 'Riverdale', 'Norwood',
       'Co-op City', 'Port Morris', 'Fordham', 'Concourse Village',
       'Mott Haven', 'Highbridge', 'Morris Park', 'Tremont', 'Mount Hope',
       'Morris Heights', 'Throgs Neck', 'West Farms', 'Pelham Bay',
       'Clason Point', 'Morrisania', 'Belmont', 'Melrose',
       'University Heights', 'Woodlawn', 'Van Nest', 'North Riverdale',
       'Schuylerville', 'Pelham Gardens', 'Olinville', 'Edenwald',
       'Baychester', 'Hunts Point', 'Claremont Village',
       'Westchester Square', 'Unionport', 'Mount Eden', 'Castle Hill',
       'Eastchester', 'East Morrisania']
}

# Create app layout

app.layout = html.Div([
    html.Div([
        html.H1("Analysis on the listings of Airbnbs in New York"),
    ]),
    html.Div([
        dcc.Graph(figure=scatter, style={'width': '90vw', 'height': '90vh'})
    ],
        style={"width": "100%","height": "100%"}),
    html.Hr(),
    html.H3('Neighbourhood listing analysis'),
    html.Div([
        html.P("Select a neighbourhood group:"),
        dcc.RadioItems(
            id='neighbourhood_group',
            options=list(all_neighbourhoods.keys()),
            value="Manhattan",
            inline=True),
        dcc.Graph(id="graph", style = {'width': '90vh', 'height': '90vh', 'display': 'inline-block'})
        ], style={'display': 'inline-block'}),
    html.Div([
        html.P("Given the selected neighbourhood group, select a neighbourhood:"),
        dcc.Dropdown(
            id='neighbourhood'),

        dcc.Graph(id="box", style = {'width': '90vh', 'height': '90vh', 'display': 'inline-block'})
    ], style={'display': 'inline-block'})

])

@app.callback(
    Output('neighbourhood', 'options'),
    Input('neighbourhood_group', 'value'))
def set_neighbourhoods_options(neighbourhood_group):
    return [{'label': i, 'value': i} for i in all_neighbourhoods[neighbourhood_group]]

@app.callback(
    Output("graph", "figure"),
    Input("neighbourhood_group", "value"))
def display_histogram(neighbourhood_group):
    data = df[df["neighbourhood_group"]==neighbourhood_group].filter(['id', 'neighbourhood', 'availability_365', 'room_type'], axis=1)
    fig = px.histogram(data, x="neighbourhood", y="availability_365", color="room_type",
                       marginal="box", barmode="group", # or violin, rug
                       labels={'neighbourhood': "Neighbourhoods in chosen  Borough",
                               'availability_365': 'Availability of listings in a year',
                               'room_type': 'Types of rooms offered'},
                       histfunc='avg', cumulative=False,histnorm=None, color_discrete_sequence=['rgb(229, 134, 6)','rgb(93, 105, 177)','rgb(165, 170, 153)','rgb(36, 121, 108)'], hover_data=data.columns)
    return fig

@app.callback(
    Output('neighbourhood', 'value'),
    Input('neighbourhood', 'options'))
def set_neighbourhood_value(options):
    return options[0]['value']


@app.callback(
    Output("box", "figure"),
    Input("neighbourhood_group", "value"),
    Input("neighbourhood", "value"))
def display_boxplot(neighbourhood_group, neighbourhood):
    d = df[(df["neighbourhood_group"]==neighbourhood_group)&(df["neighbourhood"]==neighbourhood)].filter(["minimum_nights","id"], axis=1)
    box = px.box(d, y="minimum_nights")
    return box

if __name__ == '__main__':
    app.run_server(debug=True)
