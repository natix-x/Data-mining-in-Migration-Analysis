# Data-mining-in-Crime-Analysis

## Table of contents:

- [General info](#general-info)
- [Data](#data)
- [Data analysis overview](#data-analysis-overview)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)

### General info

The aim of this project was to analyze migration-related data within the European Union. The project was carried out by a 3-person team as part of the "Data Mining" course at AGH UST. Our main goal was to identify patterns and trends in migration and investigate their correlations with key socioeconomic indicators such as employment, income, fertility rate, crime, and more. A significant part of the project focused on socio-demographic profiling of migrants — we analyzed attributes such as age, gender, education level, and employment status in order to better understand the structure of migrant populations across EU countries. The results of our work were presented during a final project session, where we discussed key findings and demonstrated selected visualizations.

A detailed documentation can be found [HERE](documentation/report.pdf), and the presentation is available [HERE](documentation/presentation.pdf).

### Data

All data used for analysis is listed and linked in [data_sources.md](data/data_sources.md)

### Data analysis overview

Main Research Question:\
How is the number of immigrants in European countries related to economic and social factors?

Main Components of the Analysis:

1. Socio-demographic Profiling of Migrants:

   - Analysis of age, gender, education level, employment status, and migration motives.

2. Migration Patterns and Flows:

   - Trends in migration over time (2012–2024), by origin and destination
   - Special focus on migration from Ukraine post-2022.
   - Mapping intra-EU vs. extra-EU flows.

3. Labor Market Impact

   - Correlation between immigration levels and employment/unemployment rates.
   - Sectoral employment analysis: which industries rely most on migrants.
   - Comparative employment data for migrants vs. locals.

4. Economic and Social Correlations

   - Correlation between migration and inflation (HICP), fertility rates, and GDP growth.
   - Time-lagged effects (e.g., fertility impact visible several years after migration peak).
   - Crime and Security Analysis:
     - Investigation of correlations between immigration and crime rates (overall and by type).

5. Comparative analysis between politically liberal and conservative countries.

   - Comparative Political Perspective
   - Division of countries into liberal vs. conservative in migration approach.
   - Cross-group comparisons on immigration levels, crime rates, GDP trends, unemployment, and fertility.

6. Clustering and Pattern Detection
   - K-means clustering based on migration, employment, and crime data.

- Identification of outliers and structural similarities between countries.

### Project structure

```
├── data/                     # Raw data (original downloaded datasets, unmodified)
│
├── data_preprocessing/       # Notebooks for data cleaning and transformation
│
├── processed_data/           # Cleaned and ready-to-analyze datasets
│
├── preliminary_analysis/     # Initial exploration: early plots
│
├── data_analysis/            # Final analysis, statistical modeling, correlation studies
│
├── documentation/            # Report, presentation

```

### Requirements

- Python 3.12+
- Data science python libraries: matplotlib, numpy, pandas, seaborn, pycountry, plotly, scikit-learn

### Setup

If you want to further explore the data:

1. First, clone this repository.
   ```sh
   git clone https://github.com/natix-x/Data-mining-in-Migration-Analysis.git
   cd Data-mining-in-Migration-Analysis
   ```
2. Activate the Virtual Environment
   ```sh
   VenvSetUp.bat
   ```
