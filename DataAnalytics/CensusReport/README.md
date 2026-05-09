# Adult Census — Income Analytics Report

An exploratory data analysis (EDA) project focused on the US Adult Census dataset to predict and analyze socioeconomic factors influencing high-income earners (>50K).

## Overview

This report dives into demographic data, education levels, and geographic origins to uncover the profile of high-income individuals in the adult population.

## Key Features

- **Demographic Profiling**: Insights into income probability by age band and gender.
- **Economic Correlates**: Analysis of "Hours per Week" vs. "Income" using Z-score outlier detection.
- **Geographic Trends**: Identifying countries with the highest proportion of top earners.
- **Professional Analytics**: Modularized into a **Streamlit** dashboard with dedicated tabs for Demographics, Education, and Advanced Analytics.

## Tech Stack

- **Libraries**: NumPy, Pandas, Matplotlib, Seaborn, Streamlit
- **Analysis**: Correlation Heatmaps, Min-Max Normalization, Feature Engineering.

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch the Dashboard

```bash
streamlit run Census_Report.py
```

## Key Findings

- **Probability by Age**: The "46-55" age band shows the highest peak for reaching the >50K income threshold.
- **Education Impact**: Clear correlation between "Education Number" and income probability.
- **Work-Life Balance**: Analysis of hours worked per week by income group reveals the correlation between labor time and financial status.
