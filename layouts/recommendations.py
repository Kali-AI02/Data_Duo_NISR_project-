
# layouts/recommendations.py
from dash import html
import dash_bootstrap_components as dbc


def get_recommendations_layout():
    layout = []

    # Introduction
    layout.append(
        html.Div([
            html.H2(" Interventions for Addressing Micronutrient Deficiencies and Stunting", style={"marginBottom": "15px"}),
            html.P(
                "Rwanda faces challenges with child malnutrition in certain high-risk districts. "
                "Our dashboard analysis highlights areas where interventions can have the greatest impact. "
                "Below are sector-specific strategies tailored to improve child nutrition and health outcomes."
            )
        ], style={"marginBottom": "30px"})
    )

    # Health Sector
    layout.append(
        dbc.Card([
            dbc.CardHeader(html.H3("💉 Health Sector Interventions")),
            dbc.CardBody([
                html.P(
                    "To ensure that children grow healthy and strong, we recommend setting up "
                    "mobile health clinics in high-risk districts like Nyabihu, Ngororero, and Musanze. "
                    "These clinics will provide regular check-ups and micronutrient supplements, "
                    "focusing on children under 35 months where stunting is most prevalent."
                ),
                html.P(
                    "Additionally, training community health workers to promote breastfeeding and provide "
                    "nutrition advice will empower families and target areas with the highest malnutrition rates."
                )
            ])
        ], style={"marginBottom": "20px"})
    )

    # Agriculture Sector
    layout.append(
        dbc.Card([
            dbc.CardHeader(html.H3("🌱 Agriculture Sector Interventions")),
            dbc.CardBody([
                html.P(
                    "Community gardens in top stunting districts will help families grow nutrient-rich crops, "
                    "reducing reliance on poor water sources and improving diet diversity."
                ),
                html.P(
                    "Supporting local farmers with seeds and training to grow diverse crops can boost food security "
                    "and strengthen the nutrition of children and mothers in regions with high malnutrition percentages."
                )
            ])
        ], style={"marginBottom": "20px"})
    )

    # Education Sector
    layout.append(
        dbc.Card([
            dbc.CardHeader(html.H3("🎓 Education Sector Interventions")),
            dbc.CardBody([
                html.P(
                    "Nutrition workshops in schools and communities will teach mothers and caregivers about healthy eating. "
                    "These workshops are particularly important in districts with low maternal education levels."
                ),
                html.P(
                    "Introducing school feeding programs using local foods ensures that children receive balanced nutrition, "
                    "supporting their growth, especially male children and those from poorer households."
                )
            ])
        ], style={"marginBottom": "20px"})
    )

    # Conclusion
    layout.append(
        html.Div([
            html.P(
                "Together, these interventions form a cohesive strategy across health, agriculture, and education sectors. "
                "By targeting high-risk districts and vulnerable children, Rwanda can make measurable progress in reducing stunting and improving overall child nutrition."
            )
        ], style={"marginTop": "30px", "fontStyle": "italic"})
    )

    return html.Div(layout, style={"padding": "20px"})
