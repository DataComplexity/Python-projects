# Books Analytics Dashboard

An end-to-end data science project analyzing a massive collection of books to identify "High Quality" literature through custom scoring algorithms and trend analysis.

## Overview

The Books Analytics project explores relationships between ratings, popularity, book length, and publication dates. It implements custom mathematical models to evaluate books beyond simple averages.

## Key Features

- **Custom Book Scoring**: Implementation of a weighted normalization algorithm (0.5 Rating + 0.4 Popularity + 0.1 Length).
- **Rolling Averages**: NumPy-based convolved rolling averages to detect rating trends over decades.
- **Rating Decay Model**: Experimental logic to compute "Decayed Ratings" based on the age of the book.
- **Interactive Explorer**: **Streamlit** dashboard with advanced sidebar filters for language, year range, and quality thresholds.
- **Visual Insights**: Multi-dimensional bubble plots (Size = Page Count) and stacked bar charts for rating tiers.

## Tech Stack

- **Libraries**: NumPy, Pandas, Matplotlib, Seaborn, Streamlit
- **Format**: Jupyter Notebook (.ipynb) & Production Script (.py)

## How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Launch the Dashboard

```bash
streamlit run BooksAnalysis_Dashboard.py
```

## Core Calculations

- **Z-Score Outlier Detection**: Identifies books with extreme page counts or ratings.
- **Min-Max Normalization**: Scales features for the custom Book Score.
- **KDE Plots**: Visualizes the density of ratings across the entire dataset.
