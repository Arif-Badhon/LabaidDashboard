#import the module needed
import dash
import dash_core_components as dcc
import dash_html_components as html
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
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div(children=[
    html.Div(className='row', #define row elements
        children=[html.Div(className='four columns div-user-controls'),
                html.Div(className='eight columns div-for-charts bg-grey')
        ]
    )
]

)
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)