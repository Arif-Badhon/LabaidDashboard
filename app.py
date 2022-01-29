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
                        html.H2("Here you will get the visualization", style={'textAlign':'center'}),
                        dcc.Graph(id='company')
                    ]
                )
        ]
    )
]

)

@app.callback(
    Output('company', 'figure'),
    Input('ListDashboard', 'value'))
def graph(ListDashboard):

    fig={}

    if ListDashboard == "Company Dashboard":
        summary = collection[collection['Region'] == 'Summary']

        total = summary[summary["Product"] == "Total"]
        month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        quantity = total[["Jan_Qnt", "Feb_Qnt", "Mar_Qnt", "Apr_Qnt", "May_Qnt", "Jun_Qnt", "Jul_Qnt", "Aug_Qnt", "Sep_Qnt", "Oct_Qnt", "Nov_Qnt", "Dec_Qnt"]]
        quantity = quantity.to_numpy()
        quantity = quantity.tolist()
        quantity = quantity[0]
        sale = total[["Jan_Sales", "Feb_Sales", "Mar_Sales", "Apr_Sales", "May_Sales", "Jun_Sales", "Jul_Sales", "Aug_Sales", "Sep_Sales", "Oct_Sales", "Nov_Sales", "Dec_Sales"]]
        sale = sale.to_numpy()
        sale = sale.tolist()
        sale = sale[0]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=month, y=quantity, mode='lines', name='Quantity'))
        fig.add_trace(go.Scatter(x=month, y=sale, mode='lines', name='Sales', yaxis="y2"))

###########################
        fig.update_layout(
    # split the x-axis to fraction of plots in
    # proportions
    #xaxis=dict(
        #domain=[0.3, 0.7]
    #),
   
    # pass the y-axis title, titlefont, color
    # and tickfont as a dictionary and store
    # it an variable yaxis
        yaxis=dict(
            title="yaxis 1",
            titlefont=dict(
                color="#0000ff"
            ),
            tickfont=dict(
                color="#0000ff"
            )
        ),
        
    # pass the y-axis 2 title, titlefont, color and
    # tickfont as a dictionary and store it an
    # variable yaxis 2
        yaxis2=dict(
            title="yaxis 2",
            titlefont=dict(
                color="#FF0000"
            ),
            tickfont=dict(
                color="#FF0000"
            ),
            anchor="free",  # specifying x - axis has to be the fixed
            overlaying="y",  # specifyinfg y - axis has to be separated
            side="right",  # specifying the side the axis should be present
            position=1  # specifying the position of the axis
        ),
    )
    #fig.update_layout(title_text="Company Dashboard", style={'textAlign':'center'})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)