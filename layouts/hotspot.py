# layouts/hotspot.py
import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

# ===================================================
# Malnutrition Hotspot Layout Function
# ===================================================
def get_layout():
    # ===== Step 1 — Load and prepare dataset =====
    fn = r"C:\Users\user\Desktop\Elysee\Data_Duo_NISR_project-\df_clean.csv"
    try:
        df_clean = pd.read_csv(fn)
    except Exception as e:
        return html.Div([
            html.H3("Error loading dataset"),
            html.P(str(e))
        ])
    
    # Ensure z-scores are numeric
    df_clean['height_for_age_zscore'] = pd.to_numeric(df_clean['height_for_age_zscore'], errors='coerce')

    # Rescale z-scores if needed (values are multiplied by 100)
    if df_clean['height_for_age_zscore'].abs().max() > 10:
        df_clean['height_for_age_zscore'] = df_clean['height_for_age_zscore'] / 100

    # Compute stunted flag
    df_clean['stunted'] = df_clean['height_for_age_zscore'] < -2.0

    # ===== Step 2 — Calculate stunting rate by district =====
    if "district_code" not in df_clean.columns or "height_for_age_zscore" not in df_clean.columns:
        return html.Div("Missing required columns in dataset: 'district_code', 'height_for_age_zscore'.")

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

    # ===== Step 4 — Load Rwanda map =====
    geo_path = r"C:\Users\user\Desktop\NISR\Hackthon\geoBoundaries-RWA-ADM2 (1).geojson"
    try:
        gdf = gpd.read_file(geo_path)
    except Exception as e:
        return html.Div([
            html.H3("Error loading GeoJSON map"),
            html.P(str(e))
        ])
    
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
