# layouts/hotspot.py
import os
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

# ===================================================
# Malnutrition Hotspot Layout Function
# ===================================================
def get_layout():
    current_dir = os.path.dirname(__file__)

    # ===== Step 1 — Load and prepare dataset =====
    dataset_path = os.path.join(current_dir, "..", "assets", "nisr_dataset1.csv")
    if not os.path.exists(dataset_path):
        return html.Div([
            html.H3("Error loading dataset"),
            html.P(f"File not found: {dataset_path}")
        ])

    df_clean = pd.read_csv(dataset_path)

    # Ensure z-scores are numeric and rescale if needed
    df_clean['height_for_age_zscore'] = pd.to_numeric(df_clean['height_for_age_zscore'], errors='coerce')
    if df_clean['height_for_age_zscore'].abs().max() > 10:
        df_clean['height_for_age_zscore'] = df_clean['height_for_age_zscore'] / 100

    # Compute stunted flag
    df_clean['stunted'] = df_clean['height_for_age_zscore'] < -2.0

    # ===== Step 2 — Calculate stunting rate by district =====
    if "district_code" not in df_clean.columns:
        return html.Div("Missing required column in dataset: 'district_code'.")

    district_stunting = (
        df_clean.groupby("district_code")["stunted"]
        .mean()
        .reset_index(name="stunting_rate")
    )
    district_stunting["stunting_rate"] *= 100  # Convert to percentage

    # ===== Step 3 — Map district codes to names =====
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
    district_stunting["district_name"] = district_stunting["district_code"].map(district_map)

    # ===== Step 4 — Load Rwanda GeoJSON map =====
    geojson_path = os.path.join(current_dir, "..", "assets", "geoBoundaries-RWA-ADM2 (1).geojson")

    
    if not os.path.exists(geojson_path):
        return html.Div([
            html.H3("Error loading GeoJSON map"),
            html.P(f"File not found: {geojson_path}")
        ])

    gdf = gpd.read_file(geojson_path)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")

    # ===== Step 5 — Clean names and merge =====
    district_stunting['district_name_clean'] = district_stunting['district_name'].str.strip().str.lower()
    gdf['shapeName_clean'] = gdf['shapeName'].str.strip().str.lower()

    gdf = gdf.merge(
        district_stunting,
        left_on='shapeName_clean',
        right_on='district_name_clean',
        how='left'
    )

    # ===== Step 6 — Interactive Choropleth Map =====
    fig = px.choropleth_map(
        gdf,
        geojson=gdf.__geo_interface__,
        locations="district_name_clean",
        featureidkey="properties.shapeName_clean",
        color="stunting_rate",
        hover_name="district_name",
        hover_data={"stunting_rate": True},
        color_continuous_scale="OrRd",
        center={"lat": -1.94, "lon": 29.87},
        zoom=6.5,
        opacity=0.7,
        title="Malnutrition Hotspots in Rwanda (Stunting Rates)"
    )

    fig.update_layout(
        margin={"r":0, "t":40, "l":0, "b":0},
        coloraxis_colorbar=dict(title="Stunting Rate (%)"),
        height=650
    )

    # ===== Step 7 — Build Dashboard Layout =====
    layout = dbc.Container([
        html.H3("🗺️ Malnutrition Hotspot Analysis"),
        html.P("This interactive map shows estimated stunting rates across Rwandan districts."),
        dcc.Graph(figure=fig, id="hotspot-map")
    ], fluid=True)

    return layout
