#import the module needed
import dash
import dash_core_components as dcc
import dash_html_components as html
from matplotlib.pyplot import title
import pymongo
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import dash_auth

#Now we need to load the data
#Our data in on the mongodb database. Database name is Dashboard and
#Collection name is MedicalData
#We import our database using pymongo

#Load the Data
link = pymongo.MongoClient("mongodb+srv://Badhon:arf123bdh@medicallabaid.qwvrw.mongodb.net/test?authSource=admin&replicaSet=atlas-16nsq1-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db = link["Dashboard"]
collection = db["MedicalData"]
collection = collection.find()
collection = pd.DataFrame(collection)
collection.drop('_id', inplace=True, axis=1)

# Initialise the app
app = dash.Dash(__name__, title="Internal Business profile Dashboard")

# Define the app
app.layout = html.Div(children=[
    html.Div(className='row', #define row elements
        children=[html.Div(className='four columns div-user-controls',
            children=[
                html.H2("Labaid Data Dashboard"),
                html.P("Please Select From Dropdown to View that Dashboard"),
                html.Div(
                    className='div-for-dropdown',
                    children=[
                        dcc.Dropdown(
                            id='ListDashboard',
                            options=["Company Dashboard", "Region Dashboard", "Category Dashboard", "Product Dashboard"],
                            multi=False,
                            style={'backgroundColor': '#1E1E1E'},
                            className='stockselector'
                        ),

                    ],
                    style={'color': '#1E1E1E'})
                ]
            ),
                html.Div(className='eight columns div-for-charts bg-grey',
                    children=[
                        html.H2("Here you will get the visualization", style={'textAlign':'center'})
                    ]
                )
        ]
    )
]

)
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)