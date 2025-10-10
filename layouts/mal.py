import pandas as pd
import geopandas as gpd
import plotly.express as px
from dash import dcc, html

def get_layout():
    # ===== Step 1 — Load dataset =====
    fn = r"C:\Users\user\Desktop\Elysee\Data_Duo_NISR_project-\assets\nisr_dataset1.csv"  # update path
    df_clean = pd.read_csv(fn)

    # ===== Step 2 — Calculate stunting rate by district =====
    district_stunting = (
        df_clean
        .groupby("district_code")["height_for_age_zscore"]
        .apply(lambda x: (x < -200).mean())  # < -2.00 z-score
        .reset_index(name="stunting_rate")
    )
    district_stunting["stunting_rate"] *= 100

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
    gdf = gpd.read_file(geo_path)
    gdf = gdf.set_crs("EPSG:4326") if gdf.crs is None else gdf

    # ===== Step 5 — Clean names and merge =====
    gdf['shapeName_clean'] = gdf['shapeName'].str.strip().str.lower()
    district_stunting['district_name_clean'] = district_stunting['district_name'].str.strip().str.lower()

    gdf = gdf.merge(
        district_stunting,
        left_on='shapeName_clean',
        right_on='district_name_clean',
        how='left'
    )

    # ===== Step 6 — Create Plotly map =====
    rwanda_geojson = gdf.__geo_interface__

    fig = px.choropleth_map(
        gdf,
        geojson=rwanda_geojson,
        locations="district_name_clean",
        featureidkey="properties.shapeName_clean",
        color="stunting_rate",
        color_continuous_scale="OrRd",
        hover_name="district_name",
        hover_data={"stunting_rate": True},
        center={"lat": -1.94, "lon": 29.87},
        zoom=6.5,
        opacity=0.7,
        title="Stunting Rates by District in Rwanda"
    )

    fig.update_layout(
        margin={"r":0, "t":40, "l":0, "b":0},
        coloraxis_colorbar=dict(title="Stunting Rate (%)")
    )

    return html.Div([
        html.H3("Malnutrition Hotspot"),
        dcc.Graph(figure=fig)
    ])
