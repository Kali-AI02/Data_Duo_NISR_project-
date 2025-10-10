# app.py
import base64
import joblib
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# ===============================
# Import layouts and recommendations
# ===============================
from layouts import stunting, mal
from layouts.recommendations import get_recommendations_layout
from layouts.model import get_layout as get_layout_model, FEATURES
from layouts.overview import get_layout_overview
from layouts.hotspot import get_layout as get_layout_hotspot

# ===============================
# Import chatbot
# ===============================
from chatbot import chatbot_btn, chatbot_box, register_callbacks

# ===============================
# Create Dash app
# ===============================
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server
app.title = "Rwanda Malnutrition Dashboard"

# ===============================
# Register chatbot callbacks
# ===============================
register_callbacks(app, FEATURES)

# ===============================
# Load trained predictive model
# ===============================
MODEL_PATH = "assets/best_stunting_model_hgb_no_impute.joblib"
LOGO_PATH = "assets/nisr_logo.png"

try:
    clf = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    clf = None

try:
    with open(LOGO_PATH, 'rb') as f:
        logo_data = base64.b64encode(f.read()).decode()
except Exception:
    logo_data = ""

# ===============================
# Navbar
# ===============================
navbar = dbc.Navbar(
    dbc.Container([
        html.Div([html.Img(src=f'data:image/png;base64,{logo_data}' if logo_data else None,
                           style={"height": "45px", "width": "auto"})],
                 className="d-flex align-items-center"),
        html.Div([
            dbc.DropdownMenu(
                label="🌐 English",
                children=[
                    dbc.DropdownMenuItem("English", href="#"),
                    dbc.DropdownMenuItem("Kinyarwanda", href="#"),
                    dbc.DropdownMenuItem("French", href="#")
                ],
                nav=True, in_navbar=True
            ),
            dbc.Nav([
                dbc.NavLink("Overview", href="/overview", active="exact"),
                dbc.NavLink("Malnutrition Hotspot", href="/hotspot", active="exact"),
                dbc.NavLink("Predictive Model", href="/model", active="exact"),
                dbc.NavLink("Stunting", href="/stunting", active="exact"),
                dbc.NavLink("Recommendations", href="/recommendations", active="exact"),
            ], pills=True, className="mt-2")
        ], className="d-flex flex-column align-items-end")
    ], fluid=True),
    color="light", dark=False, sticky="top"
)

# ===============================
# Recommendations Layout
# ===============================
recommendations_layout = get_recommendations_layout()

# ===============================
# App Layout
# ===============================
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    html.Div(id="page-content"),
    chatbot_btn,
    chatbot_box,
    dcc.Store(id="scroll-trigger", data=0),
    html.Div(id="scroll-dummy", style={"display": "none"})
])

# ===============================
# Page routing callback
# ===============================
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page(pathname):
    if pathname == "/overview":
        return get_layout_overview()
    elif pathname == "/hotspot":
        return get_layout_hotspot()
    elif pathname == "/model":
        return get_layout_model()
    elif pathname == "/stunting":
        return stunting.get_layout()
    elif pathname == "/recommendations":
        return recommendations_layout
    else:
        return html.Div([
            html.H2("Welcome to Rwanda Malnutrition Dashboard"),
            html.P("Explore insights: Overview, Hotspots, Models, and Recommendations.")
        ], style={"padding": "20px"})

# ===============================
# Predictive Model Callback
# ===============================
@app.callback(
    Output("prediction-output", "children"),
    Input("predict-btn", "n_clicks"),
    [State(f"input-{f}", "value") for f in FEATURES],
    prevent_initial_call=True
)
def predict_stunting(n_clicks, *values):
    if n_clicks is None or clf is None:
        return ""
    input_dict = {f: [v] for f, v in zip(FEATURES, values)}
    input_df = pd.DataFrame(input_dict)
    numeric_features = ['wealth_index', 'mother_bmi', 'child_current_age_months_b19']
    for col in numeric_features:
        if col in input_df.columns:
            input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
    try:
        prob = clf.predict_proba(input_df)[:, 1][0]
        return f"Predicted Stunting Probability: {prob*100:.2f}%"
    except Exception as e:
        return f"Error predicting: {e}"

# ===============================
# Register Stunting Callbacks (from layouts/stunting.py)
# ===============================
stunting.register_callbacks_stunting(app)

# ===============================
# Run app
# ===============================
if __name__ == "__main__":
    app.run(debug=False)
