# NISR 2025 Big Data Hackathon – Track 2: Ending Hidden Hunger  

## 📌 Introduction  
This project was developed as part of the **NISR 2025 Big Data Hackathon**, which engages university students in designing innovative data-driven solutions for Rwanda’s national development challenges.  

We chose **Track 2: Ending Hidden Hunger**, where the challenge is to **address micronutrient deficiencies** by mapping malnutrition hotspots, developing predictive models for malnutrition risk, analyzing root causes of stunting and deficiencies, recommending interventions, and proposing policy briefs for local implementation.  

---

## 🎯 Objectives  
- Promote youth-driven data science solutions for national development.  
- Map malnutrition hotspots using geospatial data from NISR datasets.  
- Develop predictive models to assess malnutrition risk.  
- Analyze root causes of stunting and micronutrient deficiencies.  
- Recommend interventions involving the health, agriculture, and education sectors.  
- Propose short policy briefs for local implementation to support Rwanda’s nutrition goals.  

---

## 🛠️ Methodology  
1. **Data Collection**  
   - Sources: Rwanda Demographic and Health Survey (RDHS) datasets.  

2. **Data Preprocessing & Cleaning**  
   - Handle missing values.  
   - Convert z-scores to standardized values.  
   - Define malnutrition based on thresholds (e.g., z-scores < -2).  

3. **Exploratory Data Analysis (EDA)**  
   - Analyze trends by age, districts, wealth, education, water sources, and toilet types.  

4. **Predictive Modeling**  
   - Build models to predict stunting and malnutrition risk (Random Forest, etc.).  

5. **Visualization & Tools**  
   - Interactive charts using Plotly Express:  
     - Pie charts for overall malnutrition.  
     - Bar charts for districts, age groups, and causes.  
     - Line charts for trends over time.  
   - Geospatial mapping of hotspots using GeoJSON and geopandas.  

6. **Insights & Recommendations**  
   - Identify root causes and high-risk areas.  
   - Provide sector-specific interventions and policy briefs.  

---

## 📊 Expected Deliverables  
- A **complete data science pipeline**: data loading → preprocessing → modeling → visualization.  
- An **interactive dashboard** for exploring malnutrition hotspots and trends.  
- A **predictive model** for assessing malnutrition risk.  
- **Recommendations and policy briefs** for health, agriculture, and education sectors.  

---

## 🚀 Tech Stack  
- **Languages**: Python (Pandas, NumPy, Scikit-learn)  
- **Visualization**: Plotly Express, Matplotlib  
- **Data**: NISR datasets (RDHS-based CSVs)  
- **Collaboration**: GitHub, Jupyter Notebooks  
- **Deployment**: Dash, Dash Bootstrap Components  

---

## 👥 Team  
### Team Name: Data Duos  
- Iradukunda Elysee  
- Gihozo Christian  

---

## 📌 How to Run the Project  

1. Clone this repository:  
   ```bash
   git clone https://github.com/Kali-AI02/Data_Duo_NISR_project-.git
   cd Data_Duo_NISR_project-
