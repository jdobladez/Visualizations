from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from dash import html, dcc
import dash
import plotly.graph_objects as go

import pandas as pd
#import plotly.express as px
from dash.dependencies import Input, Output



if __name__ == '__main__':
    # Create data
    df = pd.read_csv(R"C:\Users\tania\Desktop\year 3 q2\visualization\airbnb_open_data.csv", low_memory=False)
    #clean neighbourhood group
    df['neighbourhood group'] = df['neighbourhood group'].replace(['brookln'], 'Brooklyn')
    df['neighbourhood group'] = df['neighbourhood group'].replace(['manhatan'], 'Manhattan')
    #clean instant bookable -> nan to no
    df['instant_bookable'] = df['instant_bookable'].replace(['nan'], 'no')

    fig = go.Figure(data=go.Scattergeo(
        lon=df['long'],
        lat=df['lat'],
        mode='markers',
        marker_color=df['id']
    ))

    fig.update_layout(
        geo_scope='usa'
    )
    app.layout = html.Div(children=[

            html.H1(children="hello"),
            html.Div(children="description"
            ),
            dcc.Graph(
                id="graph",
                figure=fig
            )
        ])
    if __name__ == '__main__':
        app.run_server(debug=True)