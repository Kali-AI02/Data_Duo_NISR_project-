import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(_name_, external_stylesheets=[dbc.themes.BOOTSTRAP])

# -------------------------
# Dashboard knowledge base
# -------------------------
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

# -------------------------
# Layout
# -------------------------
app.layout = html.Div([
    # Chat toggle button
    html.Button("AI Chat", id="chat-btn", n_clicks=0,
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
                }),

    # Hidden Chatbox
    html.Div(id="chat-box", children=[
        # Header bar
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
    }),

    # Stores
    dcc.Store(id="scroll-trigger", data=0),
    html.Div(id="scroll-dummy", style={"display": "none"})
])

# -------------------------
# Toggle chat visibility
# -------------------------
@app.callback(
    Output("chat-box", "style"),
    Input("chat-btn", "n_clicks"),
    State("chat-box", "style"),
    prevent_initial_call=True
)
def toggle_chat(n, style):
    style["display"] = "block" if style.get("display") == "none" else "none"
    return style

# -------------------------
# Handle messages
# -------------------------
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
        # User message (right)
        messages.append(html.Div(msg, style={
            "alignSelf": "flex-end",
            "backgroundColor": "#007bff",
            "color": "white",
            "padding": "8px",
            "borderRadius": "10px",
            "marginBottom": "5px",
            "maxWidth": "80%"
        }))

        # Check if user typed a number corresponding to FAQ
        if msg.isdigit():
            idx = int(msg) - 1
            if 0 <= idx < len(faq_keys):
                ai_text = dashboard_faq[faq_keys[idx]]
            else:
                ai_text = "Sorry, I don't have an answer for that number. Please choose a number from the list."
        else:
            # Default response with numbered suggestions
            ai_text = "I don't know if I understood you well. Here is what I can help with:\n"
            for i, key in enumerate(faq_keys, 1):
                ai_text += f"{i}. {key}\n"

        # AI response (left)
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

# -------------------------
# Clientside auto-scroll
# -------------------------
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

# -------------------------
# Run app
# -------------------------
if _name_ == "_main_":
    app.run(debug=True)