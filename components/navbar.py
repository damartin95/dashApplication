
from dash import html
import dash_bootstrap_components as dbc


def navbar(): 
    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Login", href="/")),
                dbc.NavItem(dbc.NavLink("Data", href="/data")),
                dbc.NavItem(dbc.NavLink("About me", href="/aboutme")),
            ] ,
            brand="lastFM-ify",
            brand_href="/",
            color="dark",
            dark=True,
        ) 
    ])
    return layout