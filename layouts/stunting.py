# layouts/stunting.py
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import chi2_contingency

# ===============================
# Load Cleaned Dataset
# ===============================
df_clean = pd.read_csv("assets/df_clean.csv")  # use relative path for deployment

# ===============================
# Compute Stunting Indicator
# ===============================
df_clean["stunted"] = (df_clean["height_for_age_zscore"] < -2).astype(int)

# ===============================
# Helper: Interactive Pie Chart
# ===============================
def create_interactive_pie(df):
    stunting_counts = df["stunted"].value_counts().rename({0: "Not Stunted", 1: "Stunted"})
    pie_df = stunting_counts.reset_index()
    pie_df.columns = ["Status", "Count"]

    fig = px.pie(
        pie_df,
        names="Status",
        values="Count",
        color="Status",
        color_discrete_map={"Not Stunted": "#2ecc71", "Stunted": "#e74c3c"},
        hover_data=["Count"]
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="%{label}: %{value} children (%{percent})"
    )
    fig.update_layout(
        title=dict(
            text=f"National Child Stunting Distribution (Unweighted Rate: {df['stunted'].mean() * 100:.1f}%)",
            x=0.5,
            xanchor="center"
        ),
        margin=dict(t=80, b=50, l=50, r=50)
    )
    return fig

# ===============================
# Helper: Factor Importance
# ===============================
def calculate_factor_importance(df):
    factors = {
        "child_sex": "Child Sex",
        "child_current_age_months_b19": "Child Age (Months)",
        "mother_education_level": "Maternal Education",
        "wealth_index": "Wealth Index",
        "source_of_drinking_water": "Water Source",
        "toilet_type": "Toilet Facility",
        "mother_bmi": "Maternal BMI",
        "region_code": "Region",
        "mother_hemoglobin_g_dl": "Maternal Hemoglobin",
        "birth_order": "Birth Order"
    }

    factor_importance = []

    for col, name in factors.items():
        if col in df.columns:
            temp_df = df[[col, "stunted"]].dropna()
            if len(temp_df) > 0:
                contingency = pd.crosstab(temp_df[col], temp_df["stunted"])
                chi2, p, dof, expected = chi2_contingency(contingency)
                n = contingency.sum().sum()
                min_dim = min(contingency.shape) - 1
                cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
                stunting_rates = temp_df.groupby(col)["stunted"].mean() * 100
                diff = stunting_rates.max() - stunting_rates.min()
                factor_importance.append({
                    "Factor": name,
                    "Cramers_V": cramers_v,
                    "Chi2": chi2,
                    "P_Value": p,
                    "Impact_Difference_%": diff,
                    "Significant": "Yes" if p < 0.05 else "No"
                })

    importance_df = pd.DataFrame(factor_importance)
    importance_df = importance_df.sort_values("Impact_Difference_%", ascending=False)
    return importance_df

# ===============================
# Helper: Bar Chart for Factor Importance
# ===============================
def create_factor_bar_chart(importance_df, top_n=10):
    top_factors = importance_df.head(top_n)
    colors = ["#2ecc71" if sig == "Yes" else "#e74c3c" for sig in top_factors["Significant"]]

    fig = go.Figure(go.Bar(
        x=top_factors["Impact_Difference_%"],
        y=top_factors["Factor"],
        orientation="h",
        marker_color=colors,
        text=top_factors["Impact_Difference_%"].round(1),
        textposition="outside"
    ))
    fig.update_layout(
        title="Top 10 Risk Factors for Child Stunting",
        xaxis_title="Difference in Stunting Prevalence (%)",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=150, r=50, t=60, b=50)
    )
    return fig

# ===============================
# Precompute Factor Importance
# ===============================
importance_df = calculate_factor_importance(df_clean)
factor_bar_fig = create_factor_bar_chart(importance_df)

# ===============================
# Layout for Stunting Page
# ===============================
def get_layout():
    weighted_rate = (df_clean["stunted"] * df_clean["weight"]).sum() / df_clean["weight"].sum() * 100
    unweighted_rate = df_clean["stunted"].mean() * 100
    total_records = len(df_clean)

    layout = dbc.Container([
        html.H3("Stunting Analysis in Rwanda", className="text-center mb-4"),

        # Row 1: Pie chart and summary
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Stunting Overview"),
                    dbc.CardBody([
                        dcc.Graph(id="stunting-pie", figure=create_interactive_pie(df_clean)),
                        html.Div(id="stunting-click-info",
                                 style={"marginTop": "10px", "fontWeight": "bold", "textAlign": "center"})
                    ])
                ]),
                md=6
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("National Statistics"),
                    dbc.CardBody([
                        html.P(f"Weighted national stunting rate: {weighted_rate:.1f}%", className="lead"),
                        html.P(f"Unweighted national stunting rate: {unweighted_rate:.1f}%"),
                        html.P(f"Total children analyzed: {total_records}"),
                        html.Hr(),
                    ])
                ]),
                md=6
            )
        ], className="mb-4"),

        # Row 2: Factor importance bar chart
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Risk Factor Importance"),
                    dbc.CardBody([
                        dcc.Graph(id="factor-bar", figure=factor_bar_fig)
                    ])
                ])
            )
        ])
    ], fluid=True)

    return layout

# ===============================
# Callback for Pie Slice Click
# ===============================
# Remove the @app.callback decorator here.
# Instead, define a function that returns the output and register callback in app.py
def register_callbacks_stunting(app):
    @app.callback(
        Output("stunting-click-info", "children"),
        Input("stunting-pie", "clickData")
    )
    def display_click_info(clickData):
        if clickData is None:
            return ""
        label = clickData["points"][0]["label"]
        if label == "Stunted":
            count = df_clean["stunted"].sum()
            weighted = (df_clean.loc[df_clean["stunted"] == 1, "weight"].sum() / df_clean["weight"].sum()) * 100
        else:
            count = len(df_clean) - df_clean["stunted"].sum()
            weighted = (df_clean.loc[df_clean["stunted"] == 0, "weight"].sum() / df_clean["weight"].sum()) * 100
        return f"{label} children: {count:,} ({weighted:.1f}% weighted)"
