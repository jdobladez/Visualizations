from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from dash import html, dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output


if __name__ == '__main__':
    # Create data
    df = pd.read_csv(R"C:\Users\tania\Desktop\year 3 q2\visualization\airbnb_open_data.csv", low_memory=False)

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