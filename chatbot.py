
from dash import html, dcc
from dash.dependencies import Input, Output, State


chatbot_btn = html.Button("AI Chat", id="chat-btn", n_clicks=0,
    style={"position": "fixed", "bottom": "20px", "right": "20px",
           "borderRadius": "50%", "padding": "15px 20px",
           "backgroundColor": "#007bff", "color": "white",
           "border": "none", "cursor": "pointer", "zIndex": "999"}
)

chatbot_box = html.Div(id="chat-box", children=[
    html.Div("Welcome to NISR AI", style={"backgroundColor": "#007bff",
                                         "color": "white", "padding": "10px",
                                         "textAlign": "center",
                                         "borderTopLeftRadius": "10px",
                                         "borderTopRightRadius": "10px",
                                         "fontWeight": "bold"}),
    html.Div(id="chat-messages", style={"height": "350px", "overflowY": "auto",
                                        "padding": "10px", "border": "1px solid #ccc",
                                        "marginBottom": "5px", "display": "flex",
                                        "flexDirection": "column"}),
    html.Div([dcc.Input(id="chat-input", type="text", placeholder="Type a message...",
                        style={"width": "75%", "padding": "8px", "marginRight": "5px"}),
              html.Button("Send", id="send-btn", n_clicks=0)], style={"display": "flex", "padding": "5px"})
], style={"position": "fixed", "bottom": "80px", "right": "20px",
          "width": "400px", "backgroundColor": "white", "border": "1px solid #ddd",
          "borderRadius": "10px", "padding": "0px", "display": "none",
          "boxShadow": "0px 0px 15px rgba(0,0,0,0.3)", "zIndex": "998"})


FEATURE_EXPLANATIONS = {
    "wealth_index": "Wealth Index indicates the household's economic status, from poorest to richest.",
    "mother_education_level": "Mother's Education Level shows the highest schooling level the mother completed.",
    "mother_bmi": "Mother BMI (Body Mass Index) reflects nutritional status of the mother.",
    "child_current_age_months_b19": "Child Age in months is used to calculate growth and stunting indicators.",
    "source_of_drinking_water": "Source of Drinking Water describes where the household gets water (safe/unsafe).",
    "toilet_type": "Toilet Type indicates sanitation facilities available in the household.",
    "region_code": "Region Code identifies the geographic region of the household in Rwanda."
}


def register_callbacks(app, FEATURES):
    @app.callback(
        Output("chat-box", "style"),
        Input("chat-btn", "n_clicks"),
        State("chat-box", "style"),
        prevent_initial_call=True
    )
    def toggle_chat(n, style):
        style = style or {"display": "none"}
        style["display"] = "block" if style.get("display") == "none" else "none"
        return style

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

        msg = str(msg or "").strip().lower()
        if not msg:
            return messages, "", scroll_data

        messages.append(html.Div(msg, style={
            "alignSelf": "flex-end", "backgroundColor": "#007bff",
            "color": "white", "padding": "8px", "borderRadius": "10px",
            "marginBottom": "5px", "maxWidth": "80%"}))

        greetings = ["hello", "hi", "hey", "hola", "how are you"]
        if any(greet in msg for greet in greetings):
            ai_text = ("Hello! I am NISR AI 🤖.\n"
                       "I can help you explore Rwanda's malnutrition data, "
                       "view stunting predictions, and provide recommendations.\n"
                       "You can ask me about features like: " + ", ".join(FEATURES))
        elif msg.isdigit():
            num = int(msg)
            if 1 <= num <= len(FEATURES):
                feature_name = FEATURES[num - 1]
                ai_text = FEATURE_EXPLANATIONS.get(feature_name, "No explanation available for this feature.")
            else:
                ai_text = "Please select a valid number from the list."
        else:
            ai_text = ("I don't fully understand your request. "
                       "Here are things I can assist with:\n" +
                       "\n".join(f"{i}. {f}" for i, f in enumerate(FEATURES, 1)))

        messages.append(html.Div(ai_text, style={
            "alignSelf": "flex-start",
            "backgroundColor": "#e5e5e5",
            "color": "black",
            "padding": "8px",
            "borderRadius": "10px",
            "marginBottom": "5px",
            "whiteSpace": "pre-line",
            "maxWidth": "80%"}))

        scroll_data = (scroll_data or 0) + 1
        return messages, "", scroll_data
