# utils/plots.py
import pandas as pd
import numpy as np
import plotly.express as px

# Load & clean data
def load_nutrition_data(csv_path):
    df = pd.read_csv(csv_path)

    # Apply WHO plausible ranges
    df.loc[(df["height_for_age_z"] < -6) | (df["height_for_age_z"] > 6), "height_for_age_z"] = np.nan
    df.loc[(df["weight_for_height_z"] < -5) | (df["weight_for_height_z"] > 5), "weight_for_height_z"] = np.nan
    df.loc[(df["weight_for_age_z"] < -6) | (df["weight_for_age_z"] > 5), "weight_for_age_z"] = np.nan

    # Indicators
    df["stunted"] = (df["height_for_age_z"] < -2).astype(int)
    df["wasted"] = (df["weight_for_height_z"] < -2).astype(int)
    df["underweight"] = (df["weight_for_age_z"] < -2).astype(int)
    df["malnourished_any"] = ((df["stunted"] == 1) | (df["wasted"] == 1) | (df["underweight"] == 1)).astype(int)

    return df

# Bar chart by sex
def malnutrition_by_sex(csv_path):
    df = load_nutrition_data(csv_path)

    sex_summary = (
        df.groupby("child_sex")[["stunted", "wasted", "underweight", "malnourished_any"]]
        .mean() * 100
    ).reset_index()

    fig = px.bar(
        sex_summary.melt(id_vars="child_sex", var_name="Indicator", value_name="Percentage"),
        x="Indicator", y="Percentage", color="child_sex", barmode="group",
        title="Malnutrition Prevalence by Child Sex",
        labels={"Indicator": "Malnutrition Type", "Percentage": "Prevalence (%)", "child_sex": "Child Sex"}
    )
    fig.update_layout(xaxis=dict(title=None), yaxis=dict(title="Percentage (%)"))
    return fig
