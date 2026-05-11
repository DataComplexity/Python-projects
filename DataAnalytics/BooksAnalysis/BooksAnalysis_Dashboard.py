#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import streamlit as st
import io
import os


# ---------------- NumPy Functions ---------------- #
def assign_rating_tiers(ratings):
    bins = np.array([0, 3.0, 4.0, 4.5, np.inf])
    labels = np.array(['Poor', 'Average', 'Good', 'Excellent'])
    tiers = np.full(ratings.shape, 'Unknown', dtype=object)
    valid_mask = ~np.isnan(ratings)
    valid_ratings = ratings[valid_mask]
    bin_indices = np.digitize(valid_ratings, bins) - 1
    tiers[valid_mask] = labels[bin_indices]
    return tiers

def detect_outliers(arr, threshold=1):
    if np.nanstd(arr) == 0 or np.all(np.isnan(arr)):
        return np.zeros_like(arr, dtype=bool)
    z_scores = (arr - np.nanmean(arr)) / np.nanstd(arr)
    return np.abs(z_scores) > threshold

def min_max_normalize(array):
    min_val = np.nanmin(array)
    max_val = np.nanmax(array)
    if np.isnan(min_val) or np.isnan(max_val) or max_val - min_val == 0:
        return np.zeros_like(array)
    return (array - min_val) / (max_val - min_val)

def compute_score(ratings, counts, pages):
    r = np.array(ratings, dtype=float)
    c = np.array(counts, dtype=float)
    p = np.array(pages, dtype=float)
    norm_r = min_max_normalize(r)
    norm_c = min_max_normalize(c)
    norm_p = min_max_normalize(p)
    score = (0.5 * norm_r) + (0.4 * norm_c) + (0.1 * norm_p)
    return np.round(score * 10, 2)

def get_closest_books(df, target, n=5):
    if 'Average_Rating' not in df.columns:
        return pd.DataFrame()
    diffs = np.abs(df['Average_Rating'].values - target)
    indices = np.argsort(diffs)[:n]
    return df.iloc[indices]

def rolling_avg_rating(arr, window=10):
    a = np.array(arr, dtype=float)
    if len(a) == 0:
        return a
    if len(a) < window or window <= 1:
        kernel = np.ones(len(a)) / len(a)
        return np.convolve(np.nan_to_num(a), kernel, mode='same')
    kernel = np.ones(window) / window
    return np.convolve(np.nan_to_num(a), kernel, mode='same')


# ---------------- Load Data ---------------- #
@st.cache_data
def load_data(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "Books", "books.csv")
    df = pd.read_csv(path, encoding='utf-8', low_memory=False)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    df['Publication_Date'] = pd.to_datetime(df['Publication_Date'], errors='coerce', dayfirst=True)
    df['Average_Rating'] = pd.to_numeric(df['Average_Rating'], errors='coerce')
    df['Ratings_Count'] = pd.to_numeric(df['Ratings_Count'], errors='coerce')
    df['Text_Reviews_Count'] = pd.to_numeric(df['Text_Reviews_Count'], errors='coerce')
    df['Num_Pages'] = pd.to_numeric(df['Num_Pages'], errors='coerce')

    df = df.sort_values('Publication_Date').reset_index(drop=True)

    df['Rating_Tier'] = assign_rating_tiers(df['Average_Rating'].values)
    df['Is_Page_Outlier'] = detect_outliers(df['Num_Pages'].values)
    df['Is_Rating_Outlier'] = detect_outliers(df['Average_Rating'].values)
    df['Book_Score'] = compute_score(df['Average_Rating'].values,
                                     df['Ratings_Count'].values,
                                     df['Num_Pages'].values)
    df['Rolling_Avg_Rating'] = rolling_avg_rating(df['Average_Rating'].fillna(0).values)
    return df

df = load_data()


# ---------------- Sidebar / Filters ---------------- #
st.sidebar.header("Filters")

languages = sorted(df['Language_Code'].dropna().unique().tolist())
languages = ["All"] + languages
lang = st.sidebar.selectbox("Language", languages, index=0)

years_series = df['Publication_Date'].dropna().dt.year
if len(years_series) == 0:
    min_year, max_year = 1900, datetime.now().year
else:
    min_year = int(years_series.min())
    max_year = int(years_series.max())
default_start = max(min_year, max_year - 15)
year_range = st.sidebar.slider("Publication Year Range", min_year, max_year, (default_start, max_year))

min_rating = st.sidebar.slider("Minimum Average Rating", 0.0, 5.0, 0.0, step=0.1)
min_ratings_count = st.sidebar.number_input("Minimum Ratings Count", min_value=0, value=0, step=100)

filtered_df = df.copy()
if lang != "All":
    filtered_df = filtered_df[filtered_df['Language_Code'] == lang]
filtered_df = filtered_df[filtered_df['Publication_Date'].dt.year.between(year_range[0], year_range[1])]
filtered_df = filtered_df[filtered_df['Average_Rating'].fillna(0) >= min_rating]
filtered_df = filtered_df[filtered_df['Ratings_Count'].fillna(0) >= min_ratings_count]


# ---------------- Header / KPIs ---------------- #
st.title("Book Analytics Dashboard")

if st.checkbox("Show Raw Data (top 5 rows)"):
    st.dataframe(df.head())

col1, col2, col3 = st.columns(3)
col1.metric("Total Books (filtered)", len(filtered_df))
col2.metric("Avg Rating (filtered)", round(filtered_df['Average_Rating'].mean() if not filtered_df.empty else 0, 2))
top_pub = filtered_df['Publisher'].mode()[0] if (not filtered_df.empty and 'Publisher' in filtered_df.columns and len(filtered_df['Publisher'].dropna()) > 0) else "N/A"
col3.metric("Top Publisher (filtered)", top_pub)

csv_buffer = io.StringIO()
filtered_df.to_csv(csv_buffer, index=False)
st.download_button("Download CSV", csv_buffer.getvalue(), file_name="books.csv", mime="text/csv")


# ---------------- Tabs ---------------- #
tab1, tab2, tab3 = st.tabs(["NumPy Operations", "Pandas Operations", "Visual Analytics"])


# =====================================================
# ------------ NumPy Based Operations & Visuals -------
# =====================================================
with tab1:
    st.header("NumPy-based Insights (filtered data)")

    # --- Key Stats Display ---
    st.subheader("Key NumPy Statistics")
    if filtered_df.empty:
        st.info("No data for selected filters.")
    else:
        ratings = filtered_df['Average_Rating'].dropna().values
        pages = filtered_df['Num_Pages'].dropna().values

        kc1, kc2, kc3, kc4 = st.columns(4)
        kc1.metric("Non-null Ratings", int(np.count_nonzero(~np.isnan(filtered_df['Average_Rating'].values))))
        kc2.metric("Mean Rating", round(float(np.mean(ratings)), 3) if len(ratings) else "N/A")
        kc3.metric("Std Dev Rating", round(float(np.std(ratings)), 3) if len(ratings) else "N/A")
        kc4.metric("Max Review Index", int(np.argmax(filtered_df['Text_Reviews_Count'].fillna(0).values)))

        pc1, pc2 = st.columns(2)
        pc1.metric("Min Pages", int(np.nanmin(pages)) if len(pages) else "N/A")
        pc2.metric("Max Pages", int(np.nanmax(pages)) if len(pages) else "N/A")

        st.write(f"**Rolling Avg Rating (first 5 values):** {rolling_avg_rating(ratings)[:5].round(3).tolist()}")

        closest = get_closest_books(filtered_df, 4.3)
        st.subheader("Books Closest to Rating 4.3")
        st.dataframe(closest[['Title', 'Authors', 'Average_Rating']].reset_index(drop=True))

    # --- NumPy Visuals ---
    st.subheader("Top 10 Books by Average Rating")
    if not filtered_df.empty:
        top_books = filtered_df.nlargest(10, 'Average_Rating').dropna(subset=['Average_Rating'])
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(top_books['Title'].astype(str), top_books['Average_Rating'], color='skyblue')
        ax.invert_yaxis()
        ax.set_xlabel("Average Rating")
        ax.set_title("Top 10 Books by Average Rating")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Top 10 Books by Book Score")
    if not filtered_df.empty:
        top_score_books = filtered_df.nlargest(10, 'Book_Score').dropna(subset=['Book_Score'])
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.barh(top_score_books['Title'].astype(str), top_score_books['Book_Score'], color='salmon')
        ax2.invert_yaxis()
        ax2.set_xlabel("Book Score")
        ax2.set_title("Top 10 Books by Book Score")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    st.subheader("Rating Tiers Distribution")
    if not filtered_df.empty:
        rating_tier_counts = filtered_df['Rating_Tier'].value_counts()
        st.bar_chart(rating_tier_counts)

    st.subheader("Outlier Summary")
    st.write(f"Number of Page Outliers (filtered): {int(filtered_df['Is_Page_Outlier'].sum())}")
    st.write(f"Number of Rating Outliers (filtered): {int(filtered_df['Is_Rating_Outlier'].sum())}")

    st.subheader("Rolling Average Rating Over Time")
    if not filtered_df.empty and not filtered_df['Publication_Date'].dropna().empty:
        rolling_df = filtered_df.sort_values('Publication_Date')
        st.line_chart(rolling_df.set_index('Publication_Date')['Rolling_Avg_Rating'])
    else:
        st.info("No publication-date data to show rolling average.")


# =====================================================
# ---------------- Pandas Based Ops -------------------
# =====================================================
with tab2:
    st.header("Pandas Operations (filtered data)")

    st.subheader("Top Authors by Number of Books")
    if filtered_df.empty:
        st.info("No data for selected filters.")
    else:
        st.write(filtered_df['Authors'].value_counts().head(10))

    st.subheader("Top Rated Books (Min 1000 Ratings)")
    top_rated = filtered_df[filtered_df['Ratings_Count'] > 1000].sort_values(by='Average_Rating', ascending=False).head(10)
    st.write(top_rated[['Title', 'Authors', 'Average_Rating', 'Ratings_Count']])

    st.subheader("Average Rating by Publisher")
    publisher_avg = filtered_df.groupby('Publisher')['Average_Rating'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(publisher_avg)

    st.subheader("Books per Year")
    filtered_df['Year'] = filtered_df['Publication_Date'].dt.year
    books_per_year = filtered_df['Year'].value_counts().sort_index()
    st.line_chart(books_per_year)

    st.subheader("Books with Missing Data (full dataset)")
    st.write(df.isnull().sum())

    st.subheader("Average Page Count by Language")
    avg_pages = filtered_df.groupby('Language_Code')['Num_Pages'].mean().sort_values(ascending=False).head(10)
    st.bar_chart(avg_pages)

    if 'Book_Score' in filtered_df.columns and 'Publisher' in filtered_df.columns:
        filtered_df['Publisher_Rank'] = filtered_df.groupby('Publisher')['Book_Score'].rank(ascending=False, method='dense')
        st.subheader("Publisher Rank (sample)")
        st.write(filtered_df[['Title', 'Publisher', 'Book_Score', 'Publisher_Rank']].head(10))

    st.subheader("High Quality Books (Rating ≥ 4.3, Count > 10k, Pages 200–800)")
    try:
        high_quality_books = filtered_df.query(
            "Average_Rating >= 4.3 and Ratings_Count > 10000 and Num_Pages.between(200, 800)"
        )
        st.write(high_quality_books[['Title', 'Authors', 'Average_Rating', 'Ratings_Count', 'Num_Pages']].head(10))
    except Exception:
        st.info("Query had no results or was invalid for filtered data.")


# =====================================================
# --------------- Matplotlib / Seaborn Ops -----------
# =====================================================
with tab3:
    st.header("Matplotlib & Seaborn Visual Analytics (filtered data)")

    st.subheader("Top 10 Books by Score")
    if filtered_df.empty:
        st.info("No data for selected filters.")
    else:
        top_books_score = filtered_df.nlargest(10, 'Book_Score').dropna(subset=['Book_Score'])
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(top_books_score['Title'].astype(str), top_books_score['Book_Score'], color='coral')
        ax.invert_yaxis()
        ax.set_xlabel("Score")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Distribution of Ratings")
    fig, ax = plt.subplots()
    ax.hist(filtered_df['Average_Rating'].dropna(), bins=20, edgecolor='black', color='lightgreen')
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Number of Books")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Rating Trend Over Time")
    if filtered_df['Publication_Date'].dropna().empty:
        st.info("No publication date data for trend.")
    else:
        df_date = filtered_df.sort_values('Publication_Date')
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df_date['Publication_Date'], df_date['Average_Rating'], marker='o', linestyle='-')
        ax.set_xlabel("Publication Date")
        ax.set_ylabel("Average Rating")
        fig.autofmt_xdate()
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Rating vs Popularity")
    fig, ax = plt.subplots()
    ax.scatter(filtered_df['Average_Rating'], filtered_df['Ratings_Count'], alpha=0.5)
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Ratings Count")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Top 5 Languages Used (Pie)")
    lang_counts = filtered_df['Language_Code'].value_counts().head(5)
    if lang_counts.empty:
        st.info("No language data.")
    else:
        fig, ax = plt.subplots()
        ax.pie(lang_counts, labels=lang_counts.index, autopct='%1.1f%%', startangle=140)
        ax.set_title("Top 5 Languages Used")
        ax.axis('equal')
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Page Count Distribution (Boxplot)")
    fig, ax = plt.subplots()
    ax.boxplot(filtered_df['Num_Pages'].dropna())
    ax.set_ylabel("Number of Pages")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Correlation Heatmap")
    numeric_cols = ['Average_Rating', 'Ratings_Count', 'Num_Pages', 'Book_Score']
    corr_df = filtered_df[numeric_cols].dropna(how='all')
    if corr_df.shape[0] < 2:
        st.info("Not enough numeric data for correlation heatmap.")
    else:
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_df.corr(), annot=True, cmap='coolwarm', ax=ax3)
        st.pyplot(fig3)
        plt.close(fig3)

    st.subheader("Rating Tiers by Language (Stacked Bar)")
    try:
        tier_lang = pd.crosstab(filtered_df['Language_Code'], filtered_df['Rating_Tier'])
        fig, ax = plt.subplots(figsize=(10, 6))
        tier_lang.plot(kind='bar', stacked=True, ax=ax, colormap='Set3')
        ax.set_ylabel("Book Count")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)
    except Exception:
        st.info("Not enough data to build stacked bar.")

    st.subheader("Original vs Decayed Ratings Over Time")
    if filtered_df['Publication_Date'].dropna().empty:
        st.info("No publication dates for decay plot.")
    else:
        df_decay = filtered_df.copy()
        df_decay['Book_Age_Years'] = (datetime.now() - df_decay['Publication_Date']).dt.days / 365
        decay_factor = 0.02
        df_decay['Decayed_Rating'] = df_decay['Average_Rating'] * np.exp(-decay_factor * df_decay['Book_Age_Years'])
        df_sorted = df_decay.sort_values('Publication_Date')
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df_sorted['Publication_Date'], df_sorted['Average_Rating'], label='Original Rating')
        ax.plot(df_sorted['Publication_Date'], df_sorted['Decayed_Rating'], label='Decayed Rating', linestyle='--')
        ax.legend()
        fig.autofmt_xdate()
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Top 10 Authors by Average Book Score")
    try:
        top_authors = filtered_df.groupby('Authors')['Book_Score'].mean().nlargest(10)
        fig, ax = plt.subplots(figsize=(10, 4))
        top_authors.plot(kind='bar', ax=ax, color='slateblue')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)
    except Exception:
        st.info("Not enough data for top authors plot.")

    st.subheader("KDE of Average Ratings")
    if filtered_df['Average_Rating'].dropna().empty:
        st.info("No ratings available for KDE.")
    else:
        fig, ax = plt.subplots()
        filtered_df['Average_Rating'].plot(kind='kde', ax=ax)
        st.pyplot(fig)
        plt.close(fig)

    st.subheader("Bubble Plot: Rating vs Popularity (Bubble Size = Page Count)")
    fig, ax = plt.subplots()
    ax.scatter(filtered_df['Average_Rating'], filtered_df['Ratings_Count'],
               s=filtered_df['Num_Pages'].fillna(0) / 10, alpha=0.5)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Ratings Count")
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Histogram + Boxplot Subplots")
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].hist(filtered_df['Average_Rating'].dropna(), bins=20, color='lightblue')
    axs[0].set_title("Rating Distribution")
    axs[1].boxplot(filtered_df['Num_Pages'].dropna())
    axs[1].set_title("Page Count")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
