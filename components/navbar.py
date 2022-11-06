
from dash import html
import dash_bootstrap_components as dbc


def navbar(): 
    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Page 0", href="/")),
                dbc.NavItem(dbc.NavLink("Page 1", href="/page1")),
                dbc.NavItem(dbc.NavLink("Page 2", href="/page2")),
            ] ,
            brand="lastFM-ify",
            brand_href="/",
            color="dark",
            dark=True,
        ) 
    ])
    return layout