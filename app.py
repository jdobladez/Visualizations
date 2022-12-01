from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

if __name__ == '__main__':
    # Create data
    df = pd.read_csv('/home/julia/Documents/TUE/Year 2/Quartile 2/Visualizations/Data Sets/Airbnb/airbnb_open_data.csv')
    # Instantiate custom views
    def remove_dollar_sign(value):
        if pd.isna(value):
            return np.NaN
        else:
            return float(value.replace("$", "").replace(",", "").replace(" ", ""))
    df["price"] = df["price"].apply(lambda x: remove_dollar_sign(x))

    df["service fee"] = df["service fee"].apply(lambda x: remove_dollar_sign(x))

    df["last review"] = pd.to_datetime(df["last review"])

    scatterplot1 = Scatterplot("Reviews vs Price", 'review rate number', 'price', df)
    scatterplot2 = Scatterplot("g", 'x', 'y', df)

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    scatterplot1,
                    scatterplot2
                ],
            ),
        ],
    )

    # Define interactions
    @app.callback(
        Output(scatterplot1.html_id, "figure"), [
        Input("select-color-scatter-1", "value"),
        Input(scatterplot2.html_id, 'selectedData')
    ])
    def update_scatter_1(selected_color, selected_data):
        return scatterplot1.update(selected_color, selected_data)

    @app.callback(
        Output(scatterplot2.html_id, "figure"), [
        Input("select-color-scatter-2", "value"),
        Input(scatterplot1.html_id, 'selectedData')
    ])
    def update_scatter_2(selected_color, selected_data):
        return scatterplot2.update(selected_color, selected_data)


    app.run_server(debug=False, dev_tools_ui=False)