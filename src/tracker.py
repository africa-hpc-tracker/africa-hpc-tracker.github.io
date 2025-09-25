from config import Config as cfg

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import json 

import pandas as pd

import plotly.graph_objects as go

from utils import flatten_json

# Load data
with open(cfg.data_path, "r") as f:
    data = f.read()
    data = json.loads(data)

flattened_data = [flatten_json(d) for d in data]
df = pd.DataFrame(flattened_data)

def get_info(idx:int, df):
    name        = df.loc[idx, "name"] 
    country     = df.loc[idx, "location_country"]
    n_gpus      = df.loc[idx, "capacity_n_GPUs"]
    gpu_type    = df.loc[idx, "capacity_GPU_type"]
    addr        = df.loc[idx, "location_address"]
    last_update = df.loc[idx, "last_update"]
    
    info = dcc.Markdown(
        f""" 
            {name} - {str(n_gpus)}x{gpu_type}
            {addr}
            {country} 
            ({last_update})
        """,
        style={"white-space": "pre"}
        )
    return info

# for i in range(df.shape[0]):
#     print(df.loc[i, "info"])
#     print()

# Map
fig = go.Figure(data=go.Choropleth(
    locations=df['location_CN'], 
    z = df['capacity_pflops_performance'], 
    zmax=10,
    zmin=0,
    locationmode = 'ISO-3',
    colorscale = 'sunset',
    # text=df["info"],
    colorbar=dict(
            title='Compute capability (petaFLOPS)', # Title for your colorbar
            orientation='h',     # Set orientation to horizontal
            thickness=5,        # Adjust thickness as needed
        )
))

fig.update_layout(
    geo_scope='africa',
    height=600,
    #margin={"r": 0, "t": 0, "l": 0, "b": 0},
    margin={"r": 0, "t": 0, "b": 0},
    autosize=True
)
fig.update_geos(
    landcolor="beige",  # Sets the color of land areas
    oceancolor="lightblue", # Sets the color of ocean areas
    subunitcolor="darkgray", # Sets the color of country subdivisions
    lakecolor="lightblue",      # Set lake color to blue
    rivercolor="lightblue",
    showlakes=True,        # Make lakes visible
    showrivers=True,        # Make lakes visible
    showland=True,
    showocean=True,
    showsubunits=True,
    resolution=50,

)
    
# app

external_stylesheets = ["https://fonts.googleapis.com/css2?family=Tahoma&display=swap"]
app = dash.Dash("Africa HPC Tracker", external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(
        children='Africa HPC Tracker',
        style={'textAlign': 'center', 'font-family': 'Arial, sans-serif'}
    ),
    html.Div(
        id='hover-info', 
        style={'textAlign': 'center', 'font-family': 'Arial, sans-serif'}
    ),
    dcc.Graph(
        id='hpc-tracker',
        figure=fig
    ),

])

@app.callback(
    Output('hover-info', 'children'),
    Input('hpc-tracker', 'hoverData'))

def display_hover_data(hoverData):
    if hoverData:
        # Access hovered point data and display or modify other elements
        idx = hoverData['points'][0]['pointIndex']
        return get_info(idx, df)
    return "Hover over a region to display the details"

if __name__ == '__main__':
    # fig.show()
    app.run(debug=True)