# Imports from 3rd party libraries
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier, Pool
import pickle
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# import dash_design_kit as ddk
import dash_daq as daq

# Imports from this application
from app import app

# loading the model and df to extract unique categories
model = pickle.load(open("model/kickstarter_model.sav", "rb"))
df = pickle.load(open("model/kickstarter_dataframe.pkl", "rb"))
categories = sorted(df.category.unique())

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Predictions

            How much are you looking to raise for your project?

            """
        ),

        dcc.Slider(
            id='slider1',
            min=0,
            max=100000,
            step=1000,
            value=20000,
            marks={0: '0',
                   20000: '$20k',
                   40000: '$40k',
                   60000: '$60k',
                   80000: '$80k',
                   100000: '100k'},
            className='mb-3'  # this gives margin spacing to the bottom
        ),

        dcc.Markdown("", id='output1',
                     className='mb-5'),

        dcc.Markdown("What category does your project fall under?"),

        dcc.Dropdown(
            id='cat_dropdown',
            options=[
                {'label': i, 'value': i} for i in categories
            ],
            value='Young Adult',
            placeholder="Select a Category",
            className='mb-5'
        ),

        dcc.Markdown("How many days will your project be open for funding?"),

        dcc.Slider(
            id='slider2',
            min=0,
            max=60,
            step=1,
            marks={
                0: '0',
                10: '10 days',
                20: '20 days',
                30: '30 days',
                40: '40 days',
                50: '50 days',
                60: '60+ days'
            },
            value=30,
            className='mb-3'
        ),

        dcc.Markdown("", id='output2',
                     className='mb-5'),

        dcc.Markdown("Are you a Staff Pick?"),

        dcc.Dropdown(
            id='staff_pick_dropdown',
            options=[
                {'label': 'Yes', 'value': 1},
                {'label': 'No', 'value': 0}
            ],
            value=1,
            placeholder="Select Yes or No",
            className='mb-5'

)  

    ],
    md=6,
)

column2 = dbc.Col(
       className='mb-50'

)

column3 = dbc.Col(
    [
        dcc.Markdown(
            """
            Given the selected features of your project,
            your chance of success is:
            """
        ),

        daq.Gauge(
        id ='pred-gauge',
        min=0,
        max=100,
        value=80),

        dcc.Markdown("", id="predict_text", className='mb-50'),


    ],
    className='mb-50',
    md=4,
)

layout = dbc.Row([column1, column2, column3])


@app.callback(
    Output(component_id='output1', component_property='children'),
    [Input(component_id='slider1', component_property='value')]
)
def update_output_div(input_value):
    return '***You have selected to raise: ${} ***'.format(input_value)


@app.callback(
    Output(component_id='output2', component_property='children'),
    [Input(component_id='slider2', component_property='value')]
)
def update_output_div2(input_value):
    return '***Your project will be open {} days for funding***'.format(input_value)

@app.callback(
    Output(component_id='pred-gauge', component_property='value'),
    [Input(component_id='slider1', component_property='value'),
    Input(component_id='cat_dropdown', component_property='value'),
    Input(component_id='slider2', component_property='value'),
    Input(component_id='staff_pick_dropdown', component_property='value')]
)
def predict(goal, category, fundPeriodDays, staff_pick):
    """
    A function that returns the likelihood of achieving a fundraising goal 
    on Kickstarter

    Parameters
    ----------
        category: str (valid category)
        staff_pick: str ("Yes" or "No")
        goal: int (0-100000)
        fundPeriodDays: int

    Returns
    -------
        probability: float
    """
    features = {
        'category': category,
        'staff_pick': staff_pick,
        'goal': goal,
        'fundPeriodDays' : fundPeriodDays
    }

    df = pd.DataFrame(features, index=[0])

    return round((model.predict_proba(df)[0][1] * 100), 1)

@app.callback(
    Output(component_id='predict_text', component_property='children'),
    [Input(component_id='pred-gauge', component_property='value')])
def update_predict_text(gauge_val):
    return "You can expect to achieve your fundraising goal {}% of the time".format(gauge_val)