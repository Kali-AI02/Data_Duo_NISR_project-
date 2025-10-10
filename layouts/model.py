# layouts/model.py
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import joblib
import pandas as pd
import numpy as np

# ========================
# Load trained model
# ========================
MODEL_PATH = "assets/best_stunting_model_hgb_no_impute.joblib"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"⚠️ Error loading model: {e}")

# ========================
# Features
# ========================
FEATURES = [
    "wealth_index",
    "mother_education_level",
    "mother_bmi",
    "child_current_age_months_b19",
    "source_of_drinking_water",
    "toilet_type",
    "region_code"
]

# ========================
# Layout
# ========================
def get_layout():
    input_fields = []
    for feat in FEATURES:
        input_fields.append(
            dbc.Row([
                dbc.Label(feat, width=5),
                dbc.Col(
                    dcc.Input(
                        id=f"input-{feat}",
                        type="number",
                        placeholder=f"Enter {feat}",
                        debounce=True,
                        style={"width": "100%"}
                    ),
                    width=7
                )
            ], className="mb-3")
        )

    layout = dbc.Container([
        html.H3("🤖 Predict Child Stunting Risk"),
        html.P("Enter household and child characteristics to estimate stunting risk."),

        html.Div(input_fields),
        dbc.Button("Predict", id="predict-btn", color="primary", className="mt-3"),
        html.Br(), html.Br(),
        html.Div(id="prediction-output", style={"fontWeight": "bold", "fontSize": "18px"})
    ], fluid=True)

    return layout


# ========================
# Callbacks
# ========================
def register_callbacks(app):
    @app.callback(
        Output("prediction-output", "children"),
        Input("predict-btn", "n_clicks"),
        [State(f"input-{feat}", "value") for feat in FEATURES]
    )
    def predict_stunting(n_clicks, *vals):
        if not n_clicks:
            return ""

        if model is None:
            return "⚠️ Model not loaded properly."

        input_data = dict(zip(FEATURES, vals))
        df_input = pd.DataFrame([input_data])

        try:
            for col in FEATURES:
                if col not in df_input.columns:
                    df_input[col] = np.nan

            prob = model.predict_proba(df_input)[:, 1][0]
            label = model.predict(df_input)[0]

            result_text = f"Predicted stunting risk: {prob*100:.2f}%"
            if label == 1:
                return f"🚨 {result_text} — Child is likely stunted."
            else:
                return f"✅ {result_text} — Child is not likely stunted."

        except Exception as e:
            return f"⚠️ Error predicting: {e}"
