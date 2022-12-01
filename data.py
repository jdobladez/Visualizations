import plotly.express as px
import pandas as pd


def get_data():
    # Read data
    df = pd.read_csv(
        '/home/julia/Documents/TUE/Year 2/Quartile 2/Visualizations/Data Sets/Airbnb/airbnb_open_data.csv')

    # Any further data preprocessing can go her

    return df
