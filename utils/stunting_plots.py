# utils/stunting_plots.py  (modified stunting_pie_chart)
import pandas as pd
import numpy as np
import plotly.express as px

def load_stunting_data(csv_path):
    df = pd.read_csv(csv_path)
    # ... your cleaning steps ...
    return df

def stunting_pie_chart(csv_path):
    df = load_stunting_data(csv_path)

    stunting_counts = df["stunted"].value_counts().rename(index={0: "Not Stunted", 1: "Stunted"})
    unweighted_rate = df["stunted"].mean() * 100

    fig = px.pie(
        names=stunting_counts.index,
        values=stunting_counts.values,
        color=stunting_counts.index,
        color_discrete_map={"Stunted": "#fc8d62", "Not Stunted": "#66c2a5"},
        hole=0.35,  # optional donut look
        title=f"Stunting in Rwanda (Unweighted rate: {unweighted_rate:.1f}%)"
    )

    fig.update_traces(textinfo="percent+label", pull=[0, 0.05], textfont_size=14)
    fig.update_layout(
        title_x=0.5,
        font=dict(size=14),          # base font size
        showlegend=False,
        margin=dict(t=70, b=20, l=20, r=20),
        height=650                   # <-- increase figure height here
    )

    return fig
