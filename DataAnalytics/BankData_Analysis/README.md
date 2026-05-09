# Bank Marketing Campaign — Executive Analytics

A comprehensive data analysis project focused on identifying key factors that influence bank term deposit subscriptions. This project features a full statistical engine and an interactive Streamlit dashboard.

## Overview

This project analyzes a dataset of bank marketing campaigns to uncover patterns in customer behavior. By processing economic indicators and demographic data, the analysis provides actionable insights into campaign efficiency.

## Key Features

- **Statistical Engine**: Built with **NumPy** for high-performance calculation of Z-scores, correlations, and employment metrics.
- **Business Intelligence**: **Pandas**-driven insights into job categories, education levels, and monthly subscription trends.
- **Interactive Dashboard**: A **Streamlit**-powered UI that allows users to filter data by job, age, and education in real-time.
- **Visual Analytics**: Advanced heatmaps, trend lines, and distribution plots using **Matplotlib**.

## Tech Stack

- **Languages**: Python
- **Libraries**: NumPy, Pandas, Matplotlib, Streamlit
- **Environment**: Jupyter Notebook / Python Script

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch the Dashboard

```bash
streamlit run Bank-Data-Analysis.py
```

## Key Insights

- **Call Duration**: Directly correlates with subscription success.
- **Economic Indicators**: Euribor rates and employment variation significantly impact customer decision-making.
- **Demographics**: Specific age groups and job categories (e.g., students and retired) show higher subscription rates.
