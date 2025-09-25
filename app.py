import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import base64

# ===============================
# Encode logo image to base64
# ===============================
with open(r'C:\Users\user\Desktop\NISR\2025\Data_Duo_NISR_project-\nisr_logo.png', 'rb') as f:
    logo_data = base64.b64encode(f.read()).decode()

# ===============================
# Initialize app
# ===============================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Rwanda Malnutrition Dashboard"
server = app.server  # for deployment

# ===============================
# Navbar
# ===============================
navbar = dbc.Navbar(
    dbc.Container([
        # LEFT: Logo
        html.Div([
            html.Img(
                src=f'data:image/png;base64,{logo_data}',
                style={"height": "45px", "width": "auto"}
            )
        ], className="d-flex align-items-center"),

        # RIGHT: Language above + Nav buttons below
        html.Div([
            # Language dropdown (top-right)
            html.Div(
                dbc.DropdownMenu(
                    label="gb English",
                    children=[
                        dbc.DropdownMenuItem("English", href="#"),
                        dbc.DropdownMenuItem("Kinyarwanda", href="#"),
                        dbc.DropdownMenuItem("French", href="#"),
                    ],
                    nav=True,
                    in_navbar=True,
                    className="language-dropdown"
                ),
                className="d-flex justify-content-end"
            ),

            # Nav buttons (below language dropdown)
            dbc.Nav(
                [
                    dbc.NavLink("Overview", href="/overview", active="exact", className="nav-link"),
                    dbc.NavLink("Malnutrition Hotspot", href="/hotspot", active="exact", className="nav-link"),
                    dbc.NavLink("Predictive Model", href="/model", active="exact", className="nav-link"),
                    dbc.NavLink("Stunting", href="/stunting", active="exact", className="nav-link"),
                    dbc.NavLink("Recommendations", href="/recommendations", active="exact", className="nav-link"),
                ],
                className="right-nav",
                pills=True,
            )
        ], className="d-flex flex-column align-items-end")
    ], fluid=True, className="d-flex justify-content-between align-items-center"),
    color="light",
    className="custom-navbar",
    dark=False,
    sticky="top",
)

# ===============================
# Chatbot floating button + box
# ===============================
chatbot_btn = html.Button("AI Chat", id="chat-btn", n_clicks=0,
    style={
        "position": "fixed",
        "bottom": "20px",
        "right": "20px",
        "borderRadius": "50%",
        "padding": "15px 20px",
        "backgroundColor": "#007bff",
        "color": "white",
        "border": "none",
        "cursor": "pointer",
        "zIndex": "999"
    }
)

chatbot_box = html.Div(id="chat-box", children=[
    # Header
    html.Div("Welcome to NISR AI", style={
        "backgroundColor": "#007bff",
        "color": "white",
        "padding": "10px",
        "textAlign": "center",
        "borderTopLeftRadius": "10px",
        "borderTopRightRadius": "10px",
        "fontWeight": "bold"
    }),

    html.Div(id="chat-messages", style={
        "height": "350px",
        "overflowY": "auto",
        "padding": "10px",
        "border": "1px solid #ccc",
        "marginBottom": "5px",
        "display": "flex",
        "flexDirection": "column"
    }),

    html.Div([
        dcc.Input(id="chat-input", type="text", placeholder="Type a message...",
                  style={"width": "75%", "padding": "8px", "marginRight": "5px"}),
        html.Button("Send", id="send-btn", n_clicks=0)
    ], style={"display": "flex", "padding": "5px"})
], style={
    "position": "fixed",
    "bottom": "80px",
    "right": "20px",
    "width": "400px",
    "backgroundColor": "white",
    "border": "1px solid #ddd",
    "borderRadius": "10px",
    "padding": "0px",
    "display": "none",
    "boxShadow": "0px 0px 15px rgba(0,0,0,0.3)",
    "zIndex": "998"
})

# ===============================
# FAQ Knowledge Base
# ===============================
dashboard_faq = {
    "what is this dashboard": "This dashboard shows key statistics from NISR datasets.",
    "how to read charts": "Each chart shows trends over time. Hover over points to see details.",
    "what does malnutrition map show": "It highlights malnutrition hotspots using geospatial data.",
    "how to filter data": "Use the filters at the top of each chart to select year, region, or other variables.",
    "how to download data": "Click the download button on the chart to export CSV or image.",
    "who can access this dashboard": "The dashboard is accessible to NISR staff and authorized partners.",
    "what are the main indicators": "Indicators include population, malnutrition prevalence, and socio-economic metrics."
}
faq_keys = list(dashboard_faq.keys())

# ===============================
# Content Pages (Skeletons)
# ===============================
overview_layout = dbc.Container([
    html.H3("Overview"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="overview-chart1", figure={}), width=6),
        dbc.Col(dcc.Graph(id="overview-chart2", figure={}), width=6),
    ])
], fluid=True)

hotspot_layout = dbc.Container([
    html.H3("Malnutrition Hotspot"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="hotspot-chart1", figure={}), width=6),
        dbc.Col(dcc.Graph(id="hotspot-chart2", figure={}), width=6),
    ])
], fluid=True)

model_layout = dbc.Container([
    html.H3("Predictive Model"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="model-chart1", figure={}), width=6),
        dbc.Col(dcc.Graph(id="model-chart2", figure={}), width=6),
    ])
], fluid=True)

stunting_layout = dbc.Container([
    html.H3("Stunting"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="stunting-chart1", figure={}), width=6),
        dbc.Col(dcc.Graph(id="stunting-chart2", figure={}), width=6),
    ])
], fluid=True)

recommendations_layout = dbc.Container([
    html.H3("Recommendations"),
    dbc.Row([
        dbc.Col(dcc.Graph(id="recom-chart1", figure={}), width=6),
        dbc.Col(dcc.Graph(id="recom-chart2", figure={}), width=6),
    ])
], fluid=True)

# ===============================
# App Layout
# ===============================
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    html.Div(id="page-content", children=[]),
    chatbot_btn,
    chatbot_box,
    dcc.Store(id="scroll-trigger", data=0),
    html.Div(id="scroll-dummy", style={"display": "none"})
])

# ===============================
# Callbacks
# ===============================
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page(pathname):
    if pathname == "/overview":
        return overview_layout
    elif pathname == "/hotspot":
        return hotspot_layout
    elif pathname == "/model":
        return model_layout
    elif pathname == "/stunting":
        return stunting_layout
    elif pathname == "/recommendations":
        return recommendations_layout
    else:
        return html.Div([
            html.H2("Welcome to Rwanda Malnutrition Dashboard"),
            html.P("Explore insights: Overview, Hotspots, Models, and Recommendations.")
        ], style={"padding": "20px"})

# Toggle chatbot
@app.callback(
    Output("chat-box", "style"),
    Input("chat-btn", "n_clicks"),
    State("chat-box", "style"),
    prevent_initial_call=True
)
def toggle_chat(n, style):
    style["display"] = "block" if style.get("display") == "none" else "none"
    return style

# Handle chatbot messages
@app.callback(
    Output("chat-messages", "children"),
    Output("chat-input", "value"),
    Output("scroll-trigger", "data"),
    Input("send-btn", "n_clicks"),
    State("chat-input", "value"),
    State("chat-messages", "children"),
    State("scroll-trigger", "data"),
    prevent_initial_call=True
)
def handle_message(n_clicks, msg, messages, scroll_data):
    if messages is None:
        messages = []

    msg = str(msg or "").strip()
    if msg:
        messages.append(html.Div(msg, style={
            "alignSelf": "flex-end",
            "backgroundColor": "#007bff",
            "color": "white",
            "padding": "8px",
            "borderRadius": "10px",
            "marginBottom": "5px",
            "maxWidth": "80%"
        }))

        if msg.isdigit():
            idx = int(msg) - 1
            if 0 <= idx < len(faq_keys):
                ai_text = dashboard_faq[faq_keys[idx]]
            else:
                ai_text = "Sorry, I don't have an answer for that number."
        else:
            ai_text = "I don't know if I understood you well. Here is what I can help with:\n"
            for i, key in enumerate(faq_keys, 1):
                ai_text += f"{i}. {key}\n"

        messages.append(html.Div(ai_text, style={
            "alignSelf": "flex-start",
            "backgroundColor": "#e5e5e5",
            "color": "black",
            "padding": "8px",
            "borderRadius": "10px",
            "marginBottom": "5px",
            "whiteSpace": "pre-line",
            "maxWidth": "80%"
        }))

    scroll_data = (scroll_data or 0) + 1
    return messages, "", scroll_data

# Auto scroll clientside
app.clientside_callback(
    """
    function(scroll_data) {
        var chatBox = document.getElementById('chat-messages');
        if (chatBox) {
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        return 0;
    }
    """,
    Output("scroll-dummy", "children"),
    Input("scroll-trigger", "data")
)

# ===============================
# Run app
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
