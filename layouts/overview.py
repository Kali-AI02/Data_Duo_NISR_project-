
import os
import pandas as pd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

def get_layout_overview():
    
    current_dir = os.path.dirname(__file__)
    fn = os.path.join(current_dir, "..", "assets", "nisr_dataset1.csv")
    df = pd.read_csv(fn)

   
    df['height_for_age_zscore'] = df['height_for_age_zscore'] / 100
    df['weight_for_age_zscore'] = df['weight_for_age_zscore'] / 100
    df['weight_for_height_zscore'] = df['weight_for_height_zscore'] / 100
    df['bmi_for_age_zscore'] = df['bmi_for_age_zscore'] / 100

   
    df['malnourished'] = (
        (df['height_for_age_zscore'] < -2) |
        (df['weight_for_age_zscore'] < -2) |
        (df['weight_for_height_zscore'] < -2) |
        (df['bmi_for_age_zscore'] < -2)
    )


    malnutrition_counts = df['malnourished'].value_counts(normalize=True) * 100
    labels = ['Malnourished', 'Not Malnourished']
    values = [malnutrition_counts.get(True, 0), malnutrition_counts.get(False, 0)]

    pie_fig = px.pie(
        names=labels,
        values=values,
        color=labels,
        color_discrete_map={'Malnourished':'#ff9999','Not Malnourished':'#66b3ff'},
        title="Overall Malnutrition Percentage"
    )

    
    district_map = {
        11: "Nyarugenge", 12: "Gasabo", 13: "Kicukiro",
        21: "Nyanza", 22: "Gisagara", 23: "Nyaruguru", 24: "Huye",
        25: "Nyamagabe", 26: "Ruhango", 27: "Muhanga", 28: "Kamonyi",
        31: "Karongi", 32: "Rutsiro", 33: "Rubavu", 34: "Nyabihu", 35: "Ngororero",
        36: "Rusizi", 37: "Nyamasheke", 41: "Rulindo", 42: "Gakenke",
        43: "Musanze", 44: "Burera", 45: "Gicumbi", 51: "Rwamagana",
        52: "Nyagatare", 53: "Gatsibo", 54: "Kayonza", 55: "Kirehe",
        56: "Ngoma", 57: "Bugesera"
    }

    malnutrition_by_district = df.groupby('district_code')['malnourished'].mean() * 100
    malnutrition_by_district = malnutrition_by_district.reset_index()
    malnutrition_by_district['district_name'] = malnutrition_by_district['district_code'].map(district_map)

    top_10_districts = malnutrition_by_district.sort_values(by='malnourished', ascending=False).head(10)

    bar_fig = px.bar(
        top_10_districts,
        y='district_name',
        x='malnourished',
        title='Top 10 Districts by Malnutrition Percentage',
        labels={'district_name': 'District', 'malnourished': 'Percentage Malnourished'},
        color='district_name',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        orientation='h'
    )
    bar_fig.update_layout(
        xaxis_title="Percentage Malnourished",
        yaxis_title="District",
        yaxis={'categoryorder':'total ascending'},
        showlegend=False,
        template='plotly_white'
    )

    layout = dbc.Container([
        html.H3("🩺 Malnutrition Overview"),
        html.P("Overall malnutrition and top districts by prevalence."),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=pie_fig, id="overview-pie-chart"), width=6),
            dbc.Col(dcc.Graph(figure=bar_fig, id="top-districts-bar"), width=6)
        ])
    ], fluid=True)

    return layout
