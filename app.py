import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

# Initialize app with Bootstrap for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Example top bar
navbar = dbc.NavbarSimple(
    brand="Rwanda Malnutrition Dashboard",
    brand_href="#",
    color="white",
    dark=True,
    children=[
        dbc.NavItem(dbc.NavLink("Overview", href="#overview")),
        dbc.NavItem(dbc.NavLink("Map", href="#map")),
        dbc.NavItem(dbc.NavLink("Model", href="#model")),
    ]
)

# Layout
app.layout = dbc.Container([
    navbar,
    html.H1("Welcome to Rwanda Malnutrition Dashboard", id="overview"),
    html.P("Explore the undernutrition rates across provinces and see model insights."),
    # Example card section
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Average BMI"),
            dbc.CardBody(html.H4("21.3", className="card-title"))
        ]), width=3),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Undernourished Population"),
            dbc.CardBody(html.H4("15%", className="card-title"))
        ]), width=3),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Top Risk Province"),
            dbc.CardBody(html.H4("Northern", className="card-title"))
        ]), width=3),
    ], className="mb-4"),
    
    # Map placeholder
    html.Div(id="map", children=[
        dcc.Graph(id="province-map")
    ]),

    # Model feature importance
    html.Div(id="model", children=[
        dcc.Graph(id="feature-importance")
    ])
], fluid=True)

# Run server
if __name__ == "__main__":
    app.run(debug=True)
