# NISR 2025 Big Data Hackathon – Track 2: Ending Hidden Hunger  

## 📌 Introduction  
This project was developed as part of the **NISR 2025 Big Data Hackathon**. The hackathon engages university students in designing innovative data-driven solutions for Rwanda’s national development challenges.  

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
   - Sources: Rwanda Demographic and Health Survey(RDHS).  
2. **Data Preprocessing & Cleaning**  
   - Handling missing values, converting z-scores, defining malnutrition based on thresholds (e.g., z-scores < -2).  
3. **Exploratory Data Analysis (EDA)**  
   - Analyze trends by age, districts, and factors like wealth, education, water sources, and toilet types.  
4. **Predictive Modeling**  
   - We built a model to predict stunting risk (e.g., using Random Forest).  
5. **Visualization & Tools**  
   - Interactive charts: Pie for overall malnutrition, bar for age/districts/causes, line for trends over time (using Plotly Express and Matplotlib).  
   - Geospatial mapping for hotspots.  
6. **Insights & Recommendations**  
   - Identify root causes and high-risk areas.  
   - Provide sector-specific interventions and policy briefs.  

---

## 📊 Expected Deliverables  
- A **data science pipeline** (from data loading to prediction and visualization).  
- An **interactive dashboard** for viewing malnutrition hotspots and trends.  
- A **predictive model** for malnutrition risk assessment.  
- **Recommendations and policy briefs** for interventions in health, agriculture, and education sectors.  

---

## 🚀 Tech Stack  
- **Languages**: Python (Pandas, NumPy, Scikit-learn)  
- **Visualization**: Plotly Express, Matplotlib  
- **Data**: NISR datasets (e.g., RDHS-based CSV files)  
- **Collaboration**: GitHub, Jupyter Notebooks  

---

## 👥 Team  
### Team name: [Data Duos]  
- Iradukunda Elysee  
- Gihozo Christian  

---

## 📌 How to Run the Project  
1. Clone this repository:  
   ```bash
   git clone https://github.com/yourusername/nisr-hackathon-2025.git
   cd nisr-hackathon-2025
