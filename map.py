
# We import the libraries being used below

from main import app
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import geojson

# Please change the following paths below to where the data is located in your laptop
# If the path is not changed, the data will not be loaded and thus there will be an error
path_dataframe = '/home/julia/Documents/TUE/Year 2/Quartile 2/Visualizations/Data Sets/Airbnb/airbnb_open_data.csv'
path_geojson = '/home/julia/Documents/TUE/Year 2/Quartile 2/Visualizations/Data Sets/Airbnb/neighbourhoods.geojson'

# Load the data

df = pd.read_csv(path_dataframe, low_memory=False) #loads main dataframe

with open(path_geojson) as f: #loads geojson file which has geographical data
    json = geojson.load(f)

# Cleaning Data

df.columns = [col.lower().replace(" ", "_") for col in df.columns] # we change the names of the attributes
# we replace the spaces in the names of the attributes with an underscore


# The function remove_dollar_sign removes unwanted characters on the values found for different categories;
# such as price or service fees. In case there is a NaN value, it returns it as a numpy one, so it can be ignored
# by other libraries when creating visualizations or even by the numpy library when performing some in-depth analysis
# on the data.
# This function was obtained from (NGUYEN THI CAM LAI, 2022) Aribnb-preprocessing + EDA. Available at:
# https://www.kaggle.com/code/nguyenthicamlai/aribnb-preprocessing-eda (Accessed: November 29, 2022)

def remove_dollar_sign(value):
    if pd.isna(value):
        return np.NaN
    else:
        return float(value.replace("$", "").replace(",", "").replace(" ", ""))

# We call the function for the following attributes:
df["price"] = df["price"].apply(lambda x: remove_dollar_sign(x))
df["service_fee"] = df["service_fee"].apply(lambda x: remove_dollar_sign(x))


# The function rem_outliers is based on (Mulani, S., 2020) Detection and Removal of Outliers in Python – An Easy to Understand Guide.
# Available at: https://www.askpython.com/python/examples/detection-removal-outliers-in-python (Accessed: January 31, 2023)
# The function is used to clean the data and remove incongruous values in the dataset, an example could be
# there was a value that went over 400 nights needed as minimum stay, this caused issues in our visualizations
# There was another value that was -1 nights needed as minimum stay, which also caused issues
# It calculates the Interquartile range (IQR) of the values and performs the lower and upper bounds for each category,
# these bounds are used to remove any row that is not in the range between the lower and upper bounds.

def rem_outliers(col):
    q25 = df[col].quantile(q=0.25)
    q75 = df[col].quantile(q=0.75)
    intr_qr = q75-q25
    maxi = q75+(1.5*intr_qr)
    mini = q75-(1.5*intr_qr)
    if col == "minimum_nights":
        mini = 1 # we state the minimum value to be 1 because why would a listing be rented if it is not going to be used for the night
    elif col == "availability_365":
        mini = 0 # as the category states is the availability in one year, thus, 0 should be the minimum
        maxi = 365 # as the category states is the availability in one year, thus, 365 should be the maximum
    df.drop(df.loc[df[col] > maxi].index, inplace=True)
    df.drop(df.loc[df[col] < mini].index, inplace=True)
    return

# We call the function and remove any outliers in the following attributes:
rem_outliers("minimum_nights")
rem_outliers("price")
rem_outliers("number_of_reviews")
rem_outliers("review_rate_number")
rem_outliers("calculated_host_listings_count")
rem_outliers("reviews_per_month")
rem_outliers("availability_365")

# Correcting and making all neighbourhood groups be written on one way
df['neighbourhood_group'] = df['neighbourhood_group'].replace(['brookln'], 'Brooklyn')
df['neighbourhood_group'] = df['neighbourhood_group'].replace(['manhatan'], 'Manhattan')
df['neighbourhood_group'] = df['neighbourhood_group'].replace(['Staten Island'], 'Staten_Island')

df.dropna(subset=['neighbourhood', 'neighbourhood_group'], inplace=True) # remove the NaN values
df.drop_duplicates(subset=['lat','long']) # remove the duplicates based on the coordinates of listings

# all_neighbourhoods is a dictionary which includes all the neighbourhoods per each neighbourhood group, this
# helps with the callbacks and interactions between the different visualizations. It is based on the following source:
# Basic dash callbacks (no date) Plotly. Available at: https://dash.plotly.com/basic-callbacks#dash-app-with-chained-callbacks (Accessed: January 31, 2023).
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

# Calculate the satisfaction score for every neighbourhood in New York
# The formula for the statisfaction score was obtained from:
# How to calculate CSAT &amp; What it means for your business (2021) MonkeyLearn Blog. Available at: https://monkeylearn.com/blog/csat-calculation/ (Accessed: January 31, 2023).

# First create empty lists, so we can add the values during the for loop
scores = []
neighbourhoods = []
borough = []

for y in list(df["neighbourhood"].unique()):
    neighdf = df[df['neighbourhood']==y].copy()
    sum_score = neighdf['review_rate_number'].sum() # calculate the sum of all the scores in the ith neighbourhood
    number_reviews = neighdf['review_rate_number'].count() # calculate the number of reviews in the ith neighbourhood
    sat = sum_score/(5*number_reviews) #calculate the satisfaction score
    scores.append(sat) #we add the value of the satisfaction score for the neighbourhood of the ith iteration
    neighbourhoods.append(y) # we add the name of the neighbourhood of the ith iteration
    boro = neighdf['neighbourhood_group'].iloc[0] # we add the name of the borough the neighbourhood of the ith iteration belongs to
    borough.append(boro)
# create the pandas dataframe with all the values and arrays from before
chorodf = {'neighbourhood_group': borough}
chorodf = pd.DataFrame(chorodf)
chorodf['sat_score'] = scores
chorodf['neighbourhood'] = neighbourhoods


# Create the non-interactive idioms;
# The scatter map shows the prices of each listing throughout its latitude and longitude coordinates
# with a colour scale to show the difference.
# The choropleth map shows the distribution of the price within the neighbourhoods using the same
# colour scale as on the scatter map, so it is easier for the user to see the similarities.

scatter_price = px.scatter_mapbox(df, lat="lat", lon="long", color="price",
                            color_continuous_scale=px.colors.sequential.Plasma, mapbox_style="carto-positron",
                            zoom=10, title='The prices for all the listings in the Airbnb Dataset')
choro_price =  px.choropleth_mapbox(df, geojson=json, featureidkey='properties.neighbourhood',locations='neighbourhood',
             center={"lat":40.7128, "lon":-74.0060},color='price',
            color_continuous_scale=px.colors.sequential.Plasma, mapbox_style='carto-positron', zoom=10,
            title='The distribution of prices for each neighbourhood')
choro_sat = px.choropleth_mapbox(chorodf, geojson=json, featureidkey='properties.neighbourhood',locations='neighbourhood',
             center={"lat":40.7128, "lon":-74.0060},color='sat_score',
            color_continuous_scale=px.colors.sequential.Viridis, mapbox_style='carto-positron', zoom=10,
            title='The distribution of the satisfaction score per neighbourhood')


# Create the app layout

app.layout = html.Div([

    html.H1("Explore the AirBnB listings in New York", style={'textAlign': 'center', 'fontSize': 40}), # title of the app
    html.P('All the different idioms and figures created to help identify '
            'relationships or trends, can be found below. '
            'Please keep in mind while scrolling that the figures might need a few seconds '
            'to show or update after changing some values.', style={'textAlign': 'center'}), #brief description
    html.Hr(),
    html.H2('Price of listings and per neighbourhood', style={'textAlign': 'center'}), #first subtitle for price maps
    html.P('For both maps, the darkest color means that the price is low (below $200) and if its yellow the price '
           'equals $1200. Thus, the color sequence means that it goes from darker colours which represent cheaper listings '
           'to lighter colours which are more expensive. '
        'The map on the left shows every listing in the AirBnB dataset. In case of wanting to gain a better insight on a '
           'specific area, please zoom in and the points will start to separate from each other. '
           'Furthermore, the map on the right displays the distribution of price of the listings per '
           'neighbourhood. The aim of this map is to help identify patterns regarding the price.', style={'textAlign': 'center'}),
    # description and annotation regarding these two maps
    html.Div([
        dcc.Graph(figure=scatter_price, style={'width': '90vh', 'height': '90vh','display': 'inline-block'})
    ], style={'display': 'inline-block'}), # displays scatter price map on the left side
    html.Div([
        dcc.Graph(figure=choro_price, style={'width': '90vh', 'height': '90vh','display': 'inline-block'})
    ], style={'display': 'inline-block'}), # displays choropleth price map on the right side
    html.H2('Contrast between price and satisfaction in each neighbourhood', style={'textAlign': 'center'}), # second subtitle for the 3rd map
    html.Div([
        html.P("The map below exhibits the satisfaction score per neighbourhood, through a color code. In a similar manner "
               "as the last two maps, the darkest colour indicates low values; satisfaction was low and higher values "
               "mean satisfaction is higher. "
               "To indentify the neighbourhoods with the best quality-price relationship, "
               "the comparison between these 3 maps is required. As they aim to explore the data "
               "and help find the insight wanted or needed.", style={'textAlign': 'center'}),
        #description of choropleth satisfaction map
        dcc.Graph(figure=choro_sat,  style={'width': '90vw', 'height': '90vh'}) #displays choropleth satisfaction map on the center
    ]),
    html.H2('Neighbourhood listing analysis', style={'textAlign': 'center'}),
    html.Div([
        html.P("Select a neighbourhood group:"),
        dcc.RadioItems(
            id='neighbourhood_group',
            options=list(all_neighbourhoods.keys()),
            value="Brooklyn",
            inline=True),
        dcc.Graph(id="graph", style = {'width': '90vh', 'height': '90vh', 'display': 'inline-block'})
        ], style={'display': 'inline-block'}),
    html.Div([
        html.P("Given the selected neighbourhood group, select a neighbourhood:"),
        dcc.Dropdown(
            id='neighbourhood'),

        dcc.Graph(id="box", style = {'width': '90vh', 'height': '90vh', 'display': 'inline-block'})
    ], style={'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='heatmap', style={'width': '90vw', 'height': '90vh'})
    ])

])
# Perform the callbacks which cause the interaction based on following source:
# Basic dash callbacks (no date) Plotly. Available at: https://dash.plotly.com/basic-callbacks#dash-app-with-chained-callbacks (Accessed: January 31, 2023).

# This callback gives back all the possible neighbourhoods that the user can choose from in the Dropdown for the
# boxplot.
@app.callback(
    Output('neighbourhood', 'options'),
    Input('neighbourhood_group', 'value'))
def set_neighbourhoods_options(neighbourhood_group):
    return [{'label': i, 'value': i} for i in all_neighbourhoods[neighbourhood_group]]


# Creates histogram (bar chart and box plot) to show distribution of the availability in a year of listings and the
#  different room types offered in each neighbourhood from the chosen borough,

@app.callback(
    Output("graph", "figure"),
    Input("neighbourhood_group", "value"))
def display_histogram(neighbourhood_group):
    data = df[df["neighbourhood_group"]==neighbourhood_group].filter(['neighbourhood', 'availability_365', 'room_type'], axis=1)
    fig = px.histogram(data, x="neighbourhood", y="availability_365", color="room_type",
                       marginal="box", barmode="group", # or violin, rug
                       labels={'neighbourhood': "Neighbourhoods in chosen  Borough",
                               'availability_365': 'Availability of listings in a year',
                               'room_type': 'Types of rooms offered'},
                       histfunc='avg', cumulative=False,histnorm=None, color_discrete_sequence=['rgb(229, 134, 6)','rgb(93, 105, 177)','rgb(165, 170, 153)','rgb(36, 121, 108)'], hover_data=data.columns)
    return fig

# Returns as output the neighbourhood the user chose in the Dropdown
@app.callback(
    Output('neighbourhood', 'value'),
    Input('neighbourhood', 'options'))
def set_neighbourhood_value(options):
    return options[0]['value']

# Create boxplot to show distribution of minimum nights on chosen neighbourhood by the user.
@app.callback(
    Output("box", "figure"),
    Input("neighbourhood_group", "value"),
    Input("neighbourhood", "value"))
def display_boxplot(neighbourhood_group, neighbourhood):
    boxdf = df[(df["neighbourhood_group"]==neighbourhood_group)&(df["neighbourhood"]==neighbourhood)].filter(["minimum_nights"], axis=1)
    box = px.box(boxdf, y="minimum_nights", labels={'minimum_nights': 'Minimum nights'},
                 title='Distribution of minimum nights required in the neighbourhood')
    return box

# Create heatmap to show distribution of price over neighbourhoods and different room types offered depending on
# chosen borough by the user.
@app.callback(
    Output("heatmap", "figure"),
    Input("neighbourhood_group", "value")
)
def display_heatmap(neighbourhood_group):
    heatdf = df[df["neighbourhood_group"] == neighbourhood_group].filter(
        ['neighbourhood', 'price', 'room_type'], axis=1)
    heat = px.density_heatmap(heatdf, x='neighbourhood', y='room_type', z='price', histfunc='avg',histnorm=None,
                  labels={'neighbourhood': "Neighbourhoods in chosen  Borough",
                        'price': 'Price of listings in neignbourhoods',
                        'room_type': 'Types of rooms offered'},
                  title='Average price of listings per neighbourhood and types of rooms offered given the chosen Borough')
    return heat
if __name__ == '__main__':
    app.run_server(debug=True)
