import os.path
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State
from flask import Flask
import git
from second import returnNameCombination, plot_timeline_MONTH, callMeBaby
from components import navbar
from pages import page2


server = Flask(__name__)


external_stylesheets =['https://www.w3schools.com/w3css/4/w3.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(server=server, external_stylesheets=external_stylesheets)

@server.route('/git-update', methods=['POST'])
def git_update():
  repo = git.Repo('./pyanywhere')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()                                
  origin.pull()
  return '', 200



nav = navbar.navbar()

app.layout = html.Div([
    nav,
    dcc.Input(id='mbid', value='835defa77f6078c7a34c3c6ba04854c6', type="text"),
    dcc.Input(id='username', value='wuhuspringfield', type='text'),
    html.Button('Click Me', id='button'),
    html.Div(id='my-div')
])


@app.callback(
    Output('my-div', 'children'),
    [Input('button', 'n_clicks')],
    [State('mbid', 'value'),
        State('username', 'value')]
)



def update_output_div(n_clicks, mbid, username):
    output = returnNameCombination(mbid, username) 

    

    
    if True:
        df = pd.read_csv('Fruits-per-City.csv')

        fig1 = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
        fig2 = px.line(df, x="Fruit", y="Amount", color="City")
        
        graph_website = html.Div(children=[
            html.H1(children='Hello Dash'),
            html.H2(children=output),

            html.Div(children='''
                Dash: A web application framework for your data.
            '''),

            dcc.Graph(
                id='example-graph',
                figure=fig1
            ),

            html.Div(children='''
                Dash: A web application framework for your data.
            '''),

            dcc.Graph(
                id='example-graph2',
                figure=fig2
            ),

            dcc.Graph(
                id='example-graph3',
                figure=plot_timeline_MONTH(callMeBaby(mbid, username))
            ),


            

        ])

        return graph_website
    return 'You have entered "{}" and "{}" and clicked {} times. Please provide valid information'.format(mbid, username, n_clicks)







    




if __name__ == '__main__':
    app.run_server()
