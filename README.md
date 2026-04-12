# GAwC-Wind-Data-Analysis
Wind data analysis of multi-height mast measurements including time-series trends, Weibull modeling, wind rose, turbulence analysis, and wind power density estimation using Python.

# Wind Data Analysis and Visualization

This project focuses on comprehensive wind data analysis using multi-height meteorological mast data. The goal is to extract insights about wind behavior, variability, and energy potential using statistical and visualization techniques.

---

## Dataset Description

The dataset consists of wind measurements recorded at multiple heights:
- 120m
- 100m
- 80m
- 60m
- 40m

Parameters include:
- Wind Speed (m/s)
- Wind Direction (°)
- Turbulence Intensity
- Timestamp-based observations

---

## Data Preprocessing

- Removed metadata rows and cleaned column names
- Converted timestamps to datetime format
- Converted wind parameters to numeric values
- Applied filtering:
  - Wind Speed: 0–100 m/s
  - Wind Direction: 0–360°
- Handled missing and invalid values

---

## Analysis Performed

### 1. Time Series Analysis
- Smoothed wind speed trends using rolling averages
- Weekly and monthly wind speed variations

### 2. Diurnal Patterns
- Hourly wind speed averages
- Heatmap visualization of 24-hour wind variation

### 3. Statistical Analysis
- Summary statistics (mean, std, quartiles)
- Distribution plots (histograms, KDE)
- ECDF (Empirical Cumulative Distribution Function)

### 4. Weibull Distribution Fitting
- Modeled wind speed using Weibull distribution
- Estimated shape and scale parameters

### 5. Wind Shear Analysis
- Variation of wind speed with height
- Vertical wind profile visualization

### 6. Turbulence Analysis
- Relationship between wind speed and turbulence intensity

### 7. Directional Analysis
- Wind speed vs direction scatter plots
- Wind rose diagrams for directional distribution

### 8. Correlation Analysis
- Correlation of wind speeds across different heights

### 9. Data Quality Check
- Data availability percentage across heights

### 10. Wind Energy Potential
- Wind power density estimation:
  
  \[
  P = \frac{1}{2} \rho v^3
  \]

---

## Visualizations Included

- Line plots (time series)
- Heatmaps
- Histograms & KDE plots
- Scatter plots
- Box plots
- Wind rose diagrams
- Power density plots

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Windrose

---

## Key Insights

- Wind speed increases with height (wind shear effect)
- Strong correlation between wind speeds at different elevations
- Weibull distribution effectively models wind behavior
- Significant variation in wind patterns across time (daily & seasonal)

---

## Applications

- Wind energy resource assessment
- Site feasibility studies for wind farms
- Turbine placement optimization
- Atmospheric research

---

## How to Run

1. Clone the repository:
```bash
https://github.com/Tasneemsaudagar/GAwC-Wind-Data-Analysis.git
