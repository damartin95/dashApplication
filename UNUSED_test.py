import dash_bootstrap_components as dbc
import dash
from dash import Input, Output, html

app = dash.Dash()


nav_contents = [
    dbc.NavItem(dbc.NavLink("Active", href="#", active=True)),
    dbc.NavItem(dbc.NavLink("A much longer link label", href="#")),
    dbc.NavItem(dbc.NavLink("Link", href="#")),
]

nav1 = dbc.Nav(nav_contents, pills=True, fill=True)

nav2 = dbc.Nav(nav_contents, pills=True, justified=True)

navs = html.Div([nav1, html.Hr(), nav2])

app.layout = html.Div([nav1])

@app.callback(
    Output("button-clicks", "children"), [Input("button-link", "n_clicks")]
)
def show_clicks(n):
    return "Button clicked {} times".format(n)




if __name__ == '__main__':
    app.run_server()
