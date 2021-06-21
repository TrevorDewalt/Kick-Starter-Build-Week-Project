# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Improve your chances of success on Kick Starter!

            Ever wonder why some projects on Kick Starter are run away successes while others flop? Could it just be luck? Or is there a secret sauce that founders can apply to maximize results? 

            Not sure? Use our handy App to improve your chances of launching a successful Kick Starter campaign!

            Kick Starter Success uses cutting edge machine learning algorithms to allow you to prioritize features that improve your chances of success.

            Not sure what those features are or how to optimize them? Don’t worry, leave that to us. 

            Click Let’s Go below to start exploring and optimizing!


            """
        ),
        dcc.Link(dbc.Button("Let's Go", color='primary'), href='/predictions')
    ],
    md=4,
)

gapminder = px.data.gapminder()
fig = px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)

column2 = dbc.Col(
    [
        dcc.Graph(figure=fig),
    ]
)

layout = dbc.Row([column1, column2])